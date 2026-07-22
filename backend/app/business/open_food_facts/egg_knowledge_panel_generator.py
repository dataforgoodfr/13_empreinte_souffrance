import logging
import os
from copy import deepcopy
from pathlib import Path
from typing import Callable, List

from jinja2 import Environment, FileSystemLoader
from pydantic import HttpUrl

from app.enums.open_food_facts.enums import AnimalType, EggQuantity
from app.enums.open_food_facts.panel_texts import (
    DurationTexts,
    PanelTextManager,
    QuantityTexts,
    RootPanelTexts,
)
from app.schemas.open_food_facts.internal import (
    AnimalPainReport,
    Element,
    KnowledgePanelResponse,
    PainReport,
    Panel,
    PanelElement,
    ProductInfo,
    TextElement,
    TitleElement,
)

logger = logging.getLogger("app")


class PanelRenderer:
    """Renders Jinja2 HTML templates for a given locale, with the KP images base URL injected."""

    def __init__(self, env: Environment, locale: str, base_url: str):
        """
        Args:
            env: Jinja2 environment used to load templates
            locale: Locale subfolder to load templates from (e.g. "fr", "en")
            base_url: Base URL prepended to knowledge panel images in templates
        """
        self.env = env
        self.locale = locale
        self.base_url = base_url

    def render(self, template_name: str, **context) -> str:
        """
        Render the given template for the configured locale.

        Args:
            template_name: Name of the template file, relative to the locale folder
            **context: Extra variables passed to the template

        Returns:
            The rendered HTML as a string
        """
        template = self.env.get_template(f"{self.locale}/{template_name}")
        return template.render(kp_images_base_url=self.base_url, **context)


class DurationFormatter:
    """Formats a duration in seconds into a human-readable, translated string."""

    def __init__(self, text_manager: PanelTextManager):
        """
        Args:
            text_manager: Provides translated singular/plural duration texts
        """
        self.text_manager = text_manager

    def format(self, seconds: int) -> str:
        """
        Format a duration in seconds into a human-readable string
        (e.g. "2 days 3 hours"), rounded to a "friendly" precision.

        Args:
            seconds: Duration in seconds

        Returns:
            The translated, human-readable duration
        """
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

        if parts:
            return " ".join(parts)
        return self.text_manager.get_plural_text(DurationTexts.SECOND_SINGULAR, DurationTexts.SECOND_PLURAL, 0).format(
            0
        )

    def _round(self, seconds: int) -> tuple[int, int, int, int]:
        """
        Round a duration to a "human friendly" precision depending on its magnitude:
        - >= 2 days: rounded to the nearest day
        - >= 1 day: rounded to the nearest hour
        - >= 2 hours: exact hours only
        - >= 1 hour: rounded to the nearest 10 minutes
        - >= 2 minutes: exact minutes only
        - >= 1 minute: rounded to the nearest 10 seconds
        - < 1 minute: exact seconds

        Corrects for carries between rounding steps :
        60 seconds = 1 minute, 60 minutes = 1 hour, 24 hours = 1 day
        """

        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if days >= 2:
            days, hours, minutes, sec = round(seconds / 86400), 0, 0, 0
        elif days >= 1:
            days, hours, minutes, sec = (
                days,
                round((seconds - days * 86400) / 3600),
                0,
                0,
            )
        elif hours >= 2:
            days, hours, minutes, sec = days, hours, 0, 0
        elif hours >= 1:
            days, hours, minutes, sec = (
                days,
                hours,
                round((seconds - days * 86400 - hours * 3600) / 600) * 10,
                0,
            )
        elif minutes >= 2:
            days, hours, minutes, sec = days, hours, minutes, 0
        elif minutes >= 1:
            days, hours, minutes, sec = (
                days,
                hours,
                minutes,
                round(sec / 10) * 10,
            )

        # Normalize carries
        if sec == 60:
            minutes += 1
            sec = 0
        if minutes == 60:
            hours += 1
            minutes = 0
        if hours == 24:
            days += 1
            hours = 0

        return days, hours, minutes, sec


class EggKnowledgePanelGenerator:
    """
    Class responsible for generating knowledge panel responses based on pain reports.
    """

    def __init__(self, pain_reports: List[PainReport], locale: str, translator: tuple[Callable, Callable]):
        """
        Args:
            pain_reports: Pain reports to build the knowledge panel from
            locale: Locale used to select and render HTML templates
            translator: A (gettext, ngettext) tuple used for all translations
        """
        self.pain_reports = pain_reports
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
                image_url=self.pain_reports[0].product_image_url,
                name=self.pain_reports[0].product_name,
            ),
        )

    def _create_root_panel(self, detailed_panels: list[str]) -> Panel:
        """
        Create the root panel showing:
            - the product identification
            - pain levels
        It is built from html file depending on the identification case (no information,
        full information, multiple breedings...)

        Returns:
            A panel with product data and pain levels
        """
        reports = self.pain_reports
        elements: List[Element] = []

        # First case: no pain report
        if len(reports) == 1 and not reports[0].animal_pain_reports:
            elements += self._create_element_from_html("no_fresh_egg.html")
        # Second case: multiple pain reports
        elif len(reports) > 1:
            elements += self._handle_multiple_breedings(reports)
        # Third case: single pain report
        elif len(reports) == 1 and reports[0].animal_pain_reports[0].animal_type == AnimalType.LAYING_HEN:
            elements += self._handle_single_breeding(reports[0].animal_pain_reports[0])

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

    def _handle_multiple_breedings(self, reports: List[PainReport]) -> List[Element]:
        """
        Handle the case where several breeding types are reported.
        """
        elements: List[Element] = []
        btq = reports[0].animal_pain_reports[0].breeding_type_and_quantity

        # Missing quantity -> use deep copies with a mock quantity of 1
        if btq.quantity is None:
            elements += self._create_element_from_html("no_quantity.html")
            reports = deepcopy(reports)
            for report in reports:
                report.animal_pain_reports[0].breeding_type_and_quantity.quantity = EggQuantity.from_count(1)

        elements += self._create_multiple_breedings_element(reports)
        return elements

    def _handle_single_breeding(self, apr: AnimalPainReport) -> List[Element]:
        """
        Handle the case of a single breeding type: builds the appropriate elements
        depending on which data (pain levels, quantity, breeding type) is missing.
        """
        elements: List[Element] = []
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
            apr = deepcopy(apr)
            apr.breeding_type_and_quantity.quantity = EggQuantity.from_count(1)
            elements += self._create_egg_footprint_element(apr)
            return elements

        # Missing breeding type
        if btq.breeding_type is None:
            elements += self._create_element_from_html("no_breeding_type.html")

        return elements

    def _create_project_panel(self) -> Panel:
        """
        Create the static "about the project" detailed panel.

        Returns:
            A panel presenting the Suffering Footprint project
        """
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
        """
        Render a template with no extra context and wrap it in a single text element.

        Args:
            html_file: Name of the template file to render

        Returns:
            A single-item list containing the rendered text element
        """
        html = self.renderer.render(html_file)
        return [self._get_text_element(html)]

    def _create_egg_footprint_element(self, apr: AnimalPainReport) -> List[Element]:
        """
        Build the "complete footprint" text element for a single animal pain report,
        provided it has a laying hen type, a breeding type, a quantity and pain levels.

        Args:
            apr: The animal pain report to build the element from

        Returns:
            A single-item list with the rendered element, or an empty list if the
            report is missing required data
        """
        btq = apr.breeding_type_and_quantity
        if apr.animal_type != AnimalType.LAYING_HEN or not btq.breeding_type or not btq.quantity or not apr.pain_levels:
            return []
        context = self._build_egg_context(apr)
        html = self.renderer.render("complete_footprint.html", **context)
        return [self._get_text_element(html)]

    def _create_multiple_breedings_element(self, pain_reports: List[PainReport]) -> List[Element]:
        """
        Build the elements for the multiple-breeding-types case: an intro element
        followed by one footprint-with-code element per pain report.

        Args:
            pain_reports: Pain reports, one per breeding type

        Returns:
            The list of elements to display, in display order
        """
        elements = [self._get_text_element(self.renderer.render("multiple_breeding_types.html"))]
        for report in pain_reports:
            elements.extend(self._create_egg_footprint_with_code_element(report))
        return elements

    def _create_egg_footprint_with_code_element(self, pain_report: PainReport) -> List[Element]:
        """
        Build the "complete footprint with code" text element for a pain report,
        used when several breeding types are shown side by side (each with its
        breeding type code).

        Args:
            pain_report: The pain report to build the element from

        Returns:
            A single-item list with the rendered element, or an empty list if the
            report is missing required data
        """
        apr = pain_report.animal_pain_reports[0]
        btq = apr.breeding_type_and_quantity
        if apr.animal_type != AnimalType.LAYING_HEN or not btq.breeding_type or not btq.quantity:
            return []
        context = self._build_egg_context(apr)
        context["breeding_type_code"] = btq.breeding_type.code()
        html = self.renderer.render("complete_footprint_with_code.html", **context)
        return [self._get_text_element(html)]

    def _build_detailed_panels(self, detailed_panels: list[str]) -> List[Element]:
        """
        Build the "panel" elements linking to each detailed panel (e.g. project_panel),
        to be inserted into the root panel.

        Args:
            detailed_panels: IDs of the detailed panels to link to

        Returns:
            One panel element per detailed panel ID
        """
        return [
            Element(
                element_type="panel",
                panel_element=PanelElement(panel_id=panel_id),
            )
            for panel_id in detailed_panels
        ]

    def _get_text_element(self, text: str) -> Element:
        """
        Wrap a raw HTML string into a text Element.

        Args:
            text: Rendered HTML to wrap

        Returns:
            A text-type Element containing the given HTML
        """
        return Element(element_type="text", text_element=TextElement(html=text))

    def _build_egg_context(self, apr: AnimalPainReport) -> dict:
        """
        Build the Jinja2 template context (colors, icons, translated texts, pain
        durations) for a single animal pain report.

        Args:
            apr: The animal pain report to build the context from

        Returns:
            A dict of template variables, empty if no breeding type is set
        """
        btq = apr.breeding_type_and_quantity
        breeding_type = btq.breeding_type
        quantity = btq.quantity

        if breeding_type is None:
            return {}

        context = {
            "breeding_type_color": breeding_type.color(),
            "breeding_type_icon": breeding_type.icon_url(),
            "breeding_type_text": breeding_type.translated_name(self._),
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
