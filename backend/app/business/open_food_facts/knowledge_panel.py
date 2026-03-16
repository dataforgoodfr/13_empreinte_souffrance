import logging
from pathlib import Path
from typing import Callable, List

import httpx
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from pydantic import HttpUrl, ValidationError

from app.business.open_food_facts.pain_report_calculator import PainReportCalculator
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import AnimalType, EggQuantity
from app.enums.open_food_facts.panel_texts import (
    DurationTexts,
    PanelTextManager,
    QuantityTexts,
    RootPanelTexts,
)
from app.schemas.open_food_facts.external import ProductData, ProductResponse, ProductResponseSearchALicious
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


async def get_data_from_off_v3(barcode: str, locale: str) -> ProductData:
    """
    Retrieve useful product data from OFF API v3 to compute the breeding type and the quantity of animal product

    If an error occurs, we raise a ResourceNotFoundException to return a clean response to OFF

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)
    Returns:
        A ProductData containing the name, image_url, categories, labels tags and other tags
    Raises:
        ResourceNotFoundException: If the product cannot be found or data validation fails
    """
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}.json"
    product_name_with_locale = f"product_name_{locale}"

    try:
        async with httpx.AsyncClient(
            headers={"User-Agent": "my-app/1.0"},
            follow_redirects=True,
            timeout=20.0,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            json_response = response.json()

    except Exception as e:
        logger.warning(f"OFF API error: {type(e).__name__}: {e}")
        raise ResourceNotFoundException(f"Can't get product data from OFF API: {barcode}") from e

    if product := json_response.get("product"):
        if product_name_with_locale in product:
            product["product_name"] = product[product_name_with_locale]
    else:
        raise ResourceNotFoundException(f"No hits returned by OFF API: {barcode}")

    try:
        product_response = ProductResponse.model_validate(json_response)
    except Exception as e:
        logger.error(f"Failed to validate product data: {e}")
        raise ResourceNotFoundException(f"Failed to validate product data retrieved from OFF: {barcode}") from e

    return product_response.product


async def get_data_from_off_search_a_licious(barcode: str, locale: str) -> ProductData:
    """
    Retrieve useful product data from OFF search-a-licious API
    to compute the breeding type and the quantity of animal product

    If an error occurs, we raise a ResourceNotFoundException to return a clean response to OFF

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)
    Returns:
        A ProductData containing the name, image_url, categories and labels tags
    Raises:
        ResourceNotFoundException: If the product cannot be found or data validation fails
    """
    url = "https://search.openfoodfacts.org/search"
    product_name_with_locale = f"product_name_{locale}"
    tags = [
        "categories_tags",
        "labels_tags",
        "image_url",
        "product_name",
        product_name_with_locale,
        "product_quantity_unit",
        "product_quantity",
        "quantity",
        "allergens_tags",
        "ingredients_tags",
        "ingredients",
        "countries",
        "countries_tags",
    ]
    params = {"q": f"code:{barcode}", "fields": ",".join(tags)}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            json_response = response.json()
    except Exception as e:
        logger.warning(f"Can't get product data from OFF search-a-licious API: {barcode}")
        raise ResourceNotFoundException(f"Can't get product data from OFF API: {barcode}") from e

    hits = json_response.get("hits")
    if hits and isinstance(hits, list) and product_name_with_locale in hits[0]:
        hits[0]["product_name"] = hits[0][product_name_with_locale]

    try:
        product_response = ProductResponseSearchALicious.model_validate(json_response)
    except ValidationError as e:
        logger.error(f"Failed to validate product data: {e}")
        raise ResourceNotFoundException(f"Failed to validate product data retrieved from OFF: {barcode}") from e

    if not product_response.hits:
        logger.warning(f"No hits found for params: {params}")
        raise ResourceNotFoundException(f"No hits returned by OFF API: {barcode}")

    product_data = product_response.hits[0]

    return product_data


async def get_pain_reports(barcode: str, locale: str) -> List[PainReport]:
    """
    Compute the pain reports list for a product based on its barcode

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)

    Returns:
        A list of PainReport objects
    """
    # Get the product data
    product_data = await get_data_from_off_v3(barcode, locale)

    # Create calculator with the retrieved data
    calculator = PainReportCalculator(product_data)

    # Generate and return the pain report
    return calculator.get_pain_reports()


def get_knowledge_panel_response(
    pain_reports: List[PainReport], translator: tuple[Callable, Callable]
) -> KnowledgePanelResponse:
    """
    Create a complete knowledge panel response with all panels related to suffering footprint.

    Args:
        pain_reports: A list of pain reports containing all animal data and pain durations
        translator: The translation function to use for i18n

    Returns:
        A complete KnowledgePanelResponse containing root panel, intensity definitions,
        physical pain data and psychological pain data
    """
    panel_generator = KnowledgePanelGenerator(pain_reports, translator)
    return panel_generator.get_response()


class KnowledgePanelGenerator:
    """
    Class responsible for generating knowledge panel responses based on pain reports.
    """

    def __init__(self, pain_reports: List[PainReport], translator: tuple[Callable, Callable]):
        """
        Initialize the generator with a pain report and translator.

        Args:
            pain_reports: A list of pain reports containing animal data and pain durations,
                managing the case of multiple results depending on product batches
            translator: The translation function to use for i18n
        """
        # Use the first report or an empty one if no reports
        # to be modified when managing multiple reports depending on product batches
        self.pain_reports = pain_reports
        self.text_manager = PanelTextManager(translator)
        self._ = translator[0]
        self._n = translator[1]
        self.env = Environment(
            loader=FileSystemLoader(Path(__file__).resolve().parent / "html_templates"), autoescape=True
        )

    def get_response(self) -> KnowledgePanelResponse:
        """
        Create a complete knowledge panel response with all suffering footprint panels.
        Includes detailed panels only if pain data is available.
        Returns:
            A complete KnowledgePanelResponse with all necessary panels
        """
        # Defining which detailed panels are to be displayed
        if self.pain_reports == []:
            detailed_panels = []
        else:
            detailed_panels = ["project_panel"]

        # root panel depending on pain report data and detailed panels
        panels = {"root": self._create_root_panel(detailed_panels)}

        # build detailed panels that where defined
        for panel_name, panel_creator in [
            ("project_panel", self._create_project_panel),
        ]:
            if panel_name in detailed_panels:
                panels.update({panel_name: panel_creator()})

        return KnowledgePanelResponse(
            panels=panels,
            product=ProductInfo(
                image_url=self.pain_reports[0].product_image_url,
                name=self.pain_reports[0].product_name,
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
        animal_pain_reports = self.pain_reports

        # Initialize the panel with generic information message about the project
        elements = []

        if len(self.pain_reports) > 1:
            # multiple breeding stypes but no quantity
            if self.pain_reports[0].animals[0].breeding_type_and_quantity.quantity is None:
                elements += self._create_element_from_html("no_quantity.html")

                mock_animal_pain_reports = self.pain_reports.copy()

                for i in range(len(self.pain_reports)):
                    mock_animal_pain_reports[i].animals[0].breeding_type_and_quantity.quantity = EggQuantity.from_count(
                        1
                    )

                elements += self._create_multiple_breedings_element(mock_animal_pain_reports)

            else:
                elements += self._create_multiple_breedings_element(self.pain_reports)

        elif len(self.pain_reports) == 1 and self.pain_reports[0].animals[0].animal_type == AnimalType.LAYING_HEN:
            # Add breeding type and quantity from each animal pain report even if not avalable
            for animal_pain_report in animal_pain_reports[0].animals:
                if (
                    animal_pain_report.pain_levels
                    and animal_pain_report.breeding_type_and_quantity.quantity
                    and animal_pain_report.breeding_type_and_quantity.breeding_type
                ):
                    elements += self._create_egg_footprint_element(animal_pain_report)

                elif animal_pain_report.breeding_type_and_quantity.quantity is None:
                    elements += self._create_element_from_html("no_quantity.html")

                    if animal_pain_report.breeding_type_and_quantity.breeding_type is None:
                        elements += self._create_element_from_html("no_breeding_type.html")
                    else:
                        mock_animal_pain_report = animal_pain_report.copy()
                        mock_animal_pain_report.breeding_type_and_quantity.quantity = EggQuantity.from_count(1)
                        elements += self._create_egg_footprint_element(mock_animal_pain_report)

                elif animal_pain_report.breeding_type_and_quantity.breeding_type is None:
                    elements += self._create_element_from_html("no_breeding_type.html")
        else:
            elements += self._create_element_from_html("no_fresh_egg.html")

        # Build detailed panels if existing
        for detailed_panel in detailed_panels:
            elements.extend(
                [
                    Element(element_type="panel", panel_element=PanelElement(panel_id=detailed_panel)),
                ]
            )

        # Create and return the root panel
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

    def _create_project_panel(self) -> Panel:
        """
        Creates a panel from the html file"""

        html_path = Path(__file__).resolve().parent / "html_templates" / "about_the_project.html"

        html_content = self._import_html_body(html_path)
        elements = [self._get_text_element(html_content)]

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                name="suffering-footprint",
                title="En savoir plus sur l'Empreinte Souffrance",
            ),
            topics=["suffering-footprint"],
        )

    def _create_element_from_html(self, html_file: str) -> List[Element]:
        """
        Creates a panel from the html file
        """
        html_path = Path(__file__).resolve().parent / "html_templates" / html_file

        html_content = self._import_html_body(html_path)
        return [self._get_text_element(html_content)]

    def _create_egg_footprint_element(self, animal_pain_report: AnimalPainReport) -> List[Element]:
        """
        Creates a panel from the html file
        """
        breeding_type = animal_pain_report.breeding_type_and_quantity.breeding_type
        quantity = animal_pain_report.breeding_type_and_quantity.quantity

        if (
            animal_pain_report.animal_type != AnimalType.LAYING_HEN
            or not breeding_type
            or not quantity
            or not animal_pain_report.pain_levels
        ):
            return []

        else:
            context = {
                "breeding_type_color": breeding_type.color(),
                "breeding_type_icon": breeding_type.icon_url(),
                "breeeding_type_text": breeding_type.translated_name(self._),
                "quantity_text": quantity.translated_display(
                    _=self._,
                    text_manager=self.text_manager,
                    quantity_texts=QuantityTexts,
                ),
            }

            for pain_level in animal_pain_report.pain_levels:
                key = f"{pain_level.pain_type.name.lower()}_pain_{pain_level.pain_intensity.name.lower()}"
                context[key] = self._format_duration(pain_level.seconds_in_pain)

            template = self.env.get_template("complete_footprint.html")
            html = template.render(**context)

            elements = [self._get_text_element(html)]

            return elements

    def _create_egg_footprint_with_code_element(self, pain_report: PainReport):
        """
        Creates a panel from the html file
        """
        animal_type = pain_report.animals[0].animal_type
        breeding_type = pain_report.animals[0].breeding_type_and_quantity.breeding_type
        quantity = pain_report.animals[0].breeding_type_and_quantity.quantity

        if animal_type != AnimalType.LAYING_HEN or not breeding_type or not quantity:
            return []

        else:
            pain_levels = pain_report.animals[0].pain_levels

            context = {
                "breeding_type_code": breeding_type.code(),
                "breeding_type_color": breeding_type.color(),
                "breeding_type_icon": breeding_type.icon_url(),
                "breeeding_type_text": breeding_type.translated_name(self._),
                "quantity_text": quantity.translated_display(
                    _=self._,
                    text_manager=self.text_manager,
                    quantity_texts=QuantityTexts,
                ),
            }

            for pain_level in pain_levels:
                key = f"{pain_level.pain_type.name.lower()}_pain_{pain_level.pain_intensity.name.lower()}"
                context[key] = self._format_duration(pain_level.seconds_in_pain)

            template = self.env.get_template("complete_footprint_with_code.html")
            html = template.render(**context)

            elements = [self._get_text_element(html)]

            return elements

    def _create_multiple_breedings_element(self, pain_reports: List[PainReport]) -> List[Element]:
        """
        Creates a panel from the html file
        """

        html_path = Path(__file__).resolve().parent / "html_templates" / "multiple_breeding_types.html"

        html_content = self._import_html_body(html_path)
        elements = [self._get_text_element(html_content)]

        for pain_report in pain_reports:
            elements.extend(self._create_egg_footprint_with_code_element(pain_report))

        return elements

    @staticmethod
    def _import_html_body(path: Path) -> str:
        """
        Import the html body from a given path
        """

        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        body = soup.body

        return body.decode_contents() if body else ""

    @staticmethod
    def _replace_html_body(obj, html_content=None):
        """replaces {html_body} in all strings in json object"""
        if isinstance(obj, dict):
            return {k: KnowledgePanelGenerator._replace_html_body(v, html_content) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [KnowledgePanelGenerator._replace_html_body(v, html_content) for v in obj]
        elif isinstance(obj, str):
            return obj.replace("{html_body}", html_content)
        return obj

    def _get_text_element(self, text: str) -> Element:
        """
        Create a text element with HTML content for use in a panel.

        Args:
            text: The HTML content as a string

        Returns:
            An Element object with the text content properly wrapped
        """
        return Element(element_type="text", text_element=TextElement(html=text))

    def _format_duration(self, seconds: int) -> str:
        """
        Format a duration in seconds into a human-readable string.
        """
        if seconds <= 0:
            return self.text_manager.get_text(DurationTexts.ZERO_SECOND)

        days, hours, minutes, sec = self._round_duration(seconds)

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

    def _round_duration(self, seconds: int) -> tuple[int, int, int, int]:
        """
        Round the duration for better readability in the panels.
            - If the duration is more than 1 minute, we round to 10 seconds
            - If the duration is more than 2 minutes, we round to minutes
            - If the duration is more than 1 hour, we round to 10 minutes
            - If the duration is more than 2 hours, we round to hours
            - If the duration is more than 2 days, we round to days
        """
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        # round if duration is more than 2 days
        if days >= 2:
            return round(seconds / 86400), 0, 0, 0

        # round if duration is more than 1 day
        if days >= 1:
            return days, round((seconds - days * 86400) / 3600), 0, 0

        # round if duration is more than 2 hours
        if hours >= 2:
            return days, hours, 0, 0

        # round if duration is more than 1 hour
        if hours >= 1:
            return days, hours, round((seconds - hours * 3600 - days * 86400) / 600) * 10, 0

        # round if duration is more than 2 minutes
        if minutes >= 2:
            return days, hours, minutes, 0

        # round if duration is more than 1 minute
        if minutes >= 1:
            return days, hours, minutes, round(sec / 10) * 10

        else:
            return days, hours, minutes, sec
