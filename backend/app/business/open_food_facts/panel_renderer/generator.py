import logging
import os
from pathlib import Path
from typing import Callable, List

from jinja2 import Environment, FileSystemLoader
from pydantic import HttpUrl

from app.enums.open_food_facts.content.panel_texts import (
    DurationTexts,
    PanelTextManager,
    QuantityTexts,
    RootPanelTexts,
)
from app.enums.open_food_facts.enums import AnimalType, EggQuantity
from app.schemas.open_food_facts.internal import (
    AnimalPainReport,
    Element,
    KnowledgePanelResponse,
    PainReport,
    Panel,
    PanelElement,
    ProductInfo,
    Scenario,
    TextElement,
    TitleElement,
)

logger = logging.getLogger("app")


class PanelRenderer:
    def __init__(self, env: Environment, locale: str, base_url: str):
        self.env = env
        self.locale = locale
        self.base_url = base_url

    def render(self, template_name: str, **context) -> str:
        template = self.env.get_template(f"{self.locale}/{template_name}")
        return template.render(kp_images_base_url=self.base_url, **context)


class DurationFormatter:
    def __init__(self, text_manager: PanelTextManager):
        self.text_manager = text_manager

    def format(self, seconds: int) -> str:
        if seconds <= 0:
            return self.text_manager.get_text(DurationTexts.ZERO_SECOND)

        days, hours, minutes, sec = self._round(seconds)

        parts = []

        if days:
            parts.append(
                self.text_manager.get_plural_text(DurationTexts.DAY_SINGULAR, DurationTexts.DAY_PLURAL, days).format(
                    days
                )
            )
        if hours:
            parts.append(
                self.text_manager.get_plural_text(DurationTexts.HOUR_SINGULAR, DurationTexts.HOUR_PLURAL, hours).format(
                    hours
                )
            )
        if minutes:
            parts.append(
                self.text_manager.get_plural_text(
                    DurationTexts.MINUTE_SINGULAR, DurationTexts.MINUTE_PLURAL, minutes
                ).format(minutes)
            )
        if sec:
            parts.append(
                self.text_manager.get_plural_text(
                    DurationTexts.SECOND_SINGULAR, DurationTexts.SECOND_PLURAL, sec
                ).format(sec)
            )

        return (
            " ".join(parts)
            if parts
            else self.text_manager.get_plural_text(
                DurationTexts.SECOND_SINGULAR, DurationTexts.SECOND_PLURAL, 0
            ).format(0)
        )

    def _round(self, seconds: int) -> tuple[int, int, int, int]:
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days >= 2:
            return round(seconds / 86400), 0, 0, 0
        if days >= 1:
            return days, round((seconds - days * 86400) / 3600), 0, 0
        if hours >= 2:
            return days, hours, 0, 0
        if hours >= 1:
            return days, hours, round((seconds - hours * 3600 - days * 86400) / 600) * 10, 0
        if minutes >= 2:
            return days, hours, minutes, 0
        if minutes >= 1:
            return days, hours, minutes, round(sec / 10) * 10
        return days, hours, minutes, sec


class EggKnowledgePanelGenerator:
    """
    Class responsible for generating knowledge panel responses based on pain reports.
    """

    def __init__(self, pain_report: PainReport, locale: str, translator: tuple[Callable, Callable]):
        self.pain_report = pain_report
        self.text_manager = PanelTextManager(translator)
        self._, self._n = translator
        self.locale = locale

        self.env = Environment(
            loader=FileSystemLoader(Path(__file__).resolve().parent / "html_templates"),
            autoescape=True,
        )

        self.kp_images_base_url = os.getenv("KP_IMAGES_BASE_URL", "http://localhost:3000/kp")

        self.renderer = PanelRenderer(self.env, self.locale, self.kp_images_base_url)
        self.duration_formatter = DurationFormatter(self.text_manager)

    def get_response(self) -> KnowledgePanelResponse:
        """
        Create a complete knowledge panel response with all suffering footprint panels.
        Includes detailed panels only if pain data is available.
        Returns:
            A complete KnowledgePanelResponse with all necessary panels
        """
        # Defining which detailed panels are to be displayed
        detailed_panels = ["project_panel"]

        # root panel depending on pain report data and detailed panels
        panels = {"root": self._create_root_panel(detailed_panels)}

        if "project_panel" in detailed_panels:
            panels["project_panel"] = self._create_project_panel()

        return KnowledgePanelResponse(
            panels=panels,
            product=ProductInfo(
                image_url=self.pain_report.product_image_url,
                name=self.pain_report.product_name,
            ),
        )

    def _create_root_panel(self, detailed_panels: list[str]) -> Panel:
        """
        Create the root panel showing :
            - the product identification
            - pain levels
        It is built from html file depending on the identification case (no information,
        full information, multiple breedings...)

        Returns:
            A panel with product data and pain levels
        """
        scenarios = self.pain_report.scenarios
        elements = []

        # First case : no scenario (product type not identified, or not managed).
        # `scenarios` is empty when PainReportCalculator short-circuits a mixed product,
        # or when EggButNotFreshEgg builds a PainReport with no scenario at all (relying
        # on the default `scenarios=[]`); a single scenario with no animal report is the
        # other, equivalent way to express "nothing could be computed".
        if not scenarios or (len(scenarios) == 1 and not scenarios[0].animal_pain_reports):
            elements += self._create_element_from_html("no_fresh_egg.html")

        # Second case : several scenarios (breeding type/quantity varies by batch)
        elif len(scenarios) > 1:
            elements += self._handle_multiple_breedings(scenarios)

        # Third case : single scenario
        elif len(scenarios) == 1 and scenarios[0].animal_pain_reports[0].animal_type == AnimalType.LAYING_HEN:
            elements += self._handle_single_breeding(scenarios[0].animal_pain_reports[0])

        elements += self._build_detailed_panels(detailed_panels)

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                icon_url=HttpUrl("https://iili.io/3o05WOX.png"),
                name="suffering-footprint",
                subtitle=self.text_manager.get_text(RootPanelTexts.PANEL_SUBTITLE),
                title=self.text_manager.get_text(RootPanelTexts.PANEL_TITLE),
            ),
            topics=["suffering-footprint"],
        )

    def _handle_multiple_breedings(self, scenarios: List[Scenario]) -> List[Element]:
        """
        Handle multiple scenarios case (breeding type or quantity varies by batch).
        """
        elements = []
        btq = scenarios[0].animal_pain_reports[0].breeding_type_and_quantity

        # Missing quantity -> mock scenarios with quantity 1
        if btq.quantity is None:
            elements += self._create_element_from_html("no_quantity.html")

            mock_scenarios = scenarios.copy()
            for s in mock_scenarios:
                s.animal_pain_reports[0].breeding_type_and_quantity.quantity = EggQuantity.from_count(1)

            scenarios = mock_scenarios

        elements += self._create_multiple_breedings_element(scenarios)
        return elements

    def _handle_single_breeding(self, apr: AnimalPainReport) -> List[Element]:
        elements = []
        btq = apr.breeding_type_and_quantity

        # Full data
        if apr.pain_levels and btq.quantity and btq.breeding_type:
            return self._create_egg_footprint_element(apr)

        # Missing quantity
        if btq.quantity is None:
            elements += self._create_element_from_html("no_quantity.html")

            if btq.breeding_type is None:
                elements += self._create_element_from_html("no_breeding_type.html")
                return elements

            mock = apr.copy()
            mock.breeding_type_and_quantity.quantity = EggQuantity.from_count(1)
            elements += self._create_egg_footprint_element(mock)
            return elements

        # Missing breeding type
        if btq.breeding_type is None:
            elements += self._create_element_from_html("no_breeding_type.html")

        return elements

    def _create_project_panel(self) -> Panel:
        html = self.renderer.render("about_the_project.html")

        return Panel(
            elements=[self._get_text_element(html)],
            level="info",
            title_element=TitleElement(
                name="suffering-footprint",
                title="En savoir plus sur l'Empreinte Souffrance",
            ),
            topics=["suffering-footprint"],
        )

    def _create_element_from_html(self, html_file: str) -> List[Element]:
        html = self.renderer.render(html_file)
        return [self._get_text_element(html)]

    def _create_egg_footprint_element(self, apr: AnimalPainReport) -> List[Element]:
        btq = apr.breeding_type_and_quantity

        if apr.animal_type != AnimalType.LAYING_HEN or not btq.breeding_type or not btq.quantity or not apr.pain_levels:
            return []

        context = self._build_egg_context(apr)

        html = self.renderer.render("complete_footprint.html", **context)

        return [self._get_text_element(html)]

    def _create_multiple_breedings_element(self, scenarios: List[Scenario]) -> List[Element]:
        elements = [self._get_text_element(self.renderer.render("multiple_breeding_types.html"))]

        for scenario in scenarios:
            elements.extend(self._create_egg_footprint_with_code_element(scenario))

        return elements

    def _create_egg_footprint_with_code_element(self, scenario: Scenario):
        apr = scenario.animal_pain_reports[0]
        btq = apr.breeding_type_and_quantity

        if apr.animal_type != AnimalType.LAYING_HEN or not btq.breeding_type or not btq.quantity:
            return []

        context = self._build_egg_context(apr)
        context["breeding_type_code"] = btq.breeding_type.code()

        html = self.renderer.render("complete_footprint_with_code.html", **context)

        return [self._get_text_element(html)]

    def _build_detailed_panels(self, detailed_panels: list[str]) -> List[Element]:
        return [
            Element(
                element_type="panel",
                panel_element=PanelElement(panel_id=panel_id),
            )
            for panel_id in detailed_panels
        ]

    def _get_text_element(self, text: str) -> Element:
        return Element(element_type="text", text_element=TextElement(html=text))

    def _build_egg_context(self, apr: AnimalPainReport) -> dict:
        btq = apr.breeding_type_and_quantity
        breeding_type = btq.breeding_type
        quantity = btq.quantity

        if breeding_type is None:
            return {}

        context = {
            "breeding_type_color": breeding_type.color(),
            "breeding_type_icon": breeding_type.icon_url(),
            "breeeding_type_text": breeding_type.translated_name(self._),
        }

        if quantity is not None:
            context["quantity_text"] = quantity.translated_display(
                _=self._,
                text_manager=self.text_manager,
                quantity_texts=QuantityTexts,
            )

        for pain_level in apr.pain_levels:
            key = f"{pain_level.pain_type.name.lower()}_pain_{pain_level.pain_intensity.name.lower()}"
            context[key] = self.duration_formatter.format(pain_level.seconds_in_pain)

        return context
