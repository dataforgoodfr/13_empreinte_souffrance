import logging
from typing import Callable

import httpx
from pydantic import HttpUrl, ValidationError

from app.business.open_food_facts.pain_report_calculator import PainReportCalculator
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import AnimalType, PainType
from app.enums.open_food_facts.panel_texts import (
    AnimalInfoTexts,
    DurationTexts,
    IntensityDefinitionTexts,
    MainPanelTexts,
    PanelTextManager,
    PhysicalPainTexts,
    PsychologicalPainTexts,
)
from app.schemas.open_food_facts.external import ProductData, ProductResponse, ProductResponseSearchALicious
from app.schemas.open_food_facts.internal import (
    AnimalPainReport,
    BreedingTypeAndQuantity,
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
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            json_response = response.json()
    except Exception as e:
        logger.warning(f"Can't get product data from OFF API: {barcode}")
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
        logger.warning(f"Can't get product data from OFF API: {barcode}")
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


async def get_pain_report(barcode: str, locale: str) -> PainReport:
    """
    Compute the pain report for a product based on its barcode.

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)

    Returns:
        The PainReport
    """
    # Get the product data
    product_data = await get_data_from_off_v3(barcode, locale)

    # Create calculator with the retrieved data
    calculator = PainReportCalculator(product_data)

    # Generate and return the pain report
    return calculator.get_pain_report()


def get_knowledge_panel_response(
    pain_report: PainReport, translator: tuple[Callable, Callable]
) -> KnowledgePanelResponse:
    """
    Create a complete knowledge panel response with all panels related to suffering footprint.

    Args:
        pain_report: The pain report containing all animal data and pain durations
        translator: The translation function to use for i18n

    Returns:
        A complete KnowledgePanelResponse containing main panel, intensity definitions,
        physical pain data and psychological pain data
    """
    panel_generator = KnowledgePanelGenerator(pain_report, translator)
    return panel_generator.get_response()


class KnowledgePanelGenerator:
    """
    Class responsible for generating knowledge panel responses based on pain reports.
    """

    def __init__(self, pain_report: PainReport, translator: tuple[Callable, Callable]):
        """
        Initialize the generator with a pain report and translator.

        Args:
            pain_report: The pain report containing animal data and pain durations
            translator: The translation function to use for i18n
        """
        self.pain_report = pain_report
        self.text_manager = PanelTextManager(translator)
        self._ = translator[0]
        self._n = translator[1]

    def get_response(self) -> KnowledgePanelResponse:
        """
        Create a complete knowledge panel response with all suffering footprint panels.
        Includes detailed panels only if pain data is available.
        Returns:
            A complete KnowledgePanelResponse with all necessary panels
        """
        # main panel depending on pain report data
        panels = {"main": self._create_main_panel()}

        # detailed panels only if there are pain levels
        if self.pain_report.animals and any(animal.pain_levels for animal in self.pain_report.animals):
            panels.update(
                {
                    "intensities_definitions": self._create_intensities_definitions_panel(),
                    "physical_pain": self._create_physical_pain_panel(),
                    "psychological_pain": self._create_psychological_pain_panel(),
                }
            )

        return KnowledgePanelResponse(
            panels=panels,
            product=ProductInfo(
                image_url=self.pain_report.product_image_url,
                name=self.pain_report.product_name,
            ),
        )

    def _create_main_panel(self) -> Panel:
        """
        Create the main panel showing general information about the suffering footprint.

        This panel includes an explanation of the suffering footprint, the breeding
        type and animal product quantity information, and links to the other panels.
        It handles different cases of pain report data to display appropriate messages.

        Returns:
            A panel with general information and links to detailed panels
        """
        animals = self.pain_report.animals

        # Initialize the panel with generic information message about the project
        elements = [
            self._get_text_element(self.text_manager.get_text(MainPanelTexts.WELFARE_FOOTPRINT_INTRO)),
            self._get_text_element(self.text_manager.get_text(MainPanelTexts.WELFARE_FOOTPRINT_UNIQUENESS)),
        ]

        # If all animal pain reports contain no pain levels, add a missing data message
        if all(not animal.pain_levels for animal in animals):
            elements.append(self._get_text_element(self.text_manager.get_text(MainPanelTexts.MISSING_DATA)))

        # If pain levels are available, add a message explaining suffering is based on breeding type and quantity
        else:
            elements.append(self._get_text_element(self.text_manager.get_text(MainPanelTexts.DATA_BASED_ON)))

        # Add breeding type and quantity from each animal pain report aven if not avalable
        for animal in animals:
            elements.append(
                self._get_text_element(
                    self._get_breeding_type_and_quantity_html(animal.animal_type, animal.breeding_type_and_quantity)
                )
            )

        # Add links to detailed panels if existing
        elements.extend(
            [
                Element(element_type="panel", panel_element=PanelElement(panel_id="intensities_definitions")),
                Element(element_type="panel", panel_element=PanelElement(panel_id="physical_pain")),
                Element(element_type="panel", panel_element=PanelElement(panel_id="psychological_pain")),
            ]
        )

        # Create and return the main panel
        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                grade="c",
                icon_url=HttpUrl("https://iili.io/3o05WOX.png"),
                name="suffering-footprint",
                subtitle=self.text_manager.get_text(MainPanelTexts.PANEL_SUBTITLE),
                title=self.text_manager.get_text(MainPanelTexts.PANEL_TITLE),
                type="grade",
            ),
            topics=["suffering-footprint"],
        )

    def _create_intensities_definitions_panel(self) -> Panel:
        """
        Create a panel explaining the different pain intensity levels.

        This panel provides detailed definitions for each pain intensity level:
        Agonie (Excruciating), Souffrance (Disabling), Douleur (Hurtful), and Inconfort (Annoying).
        The definitions help users understand the severity of each level.

        Returns:
            A panel with definitions for each pain intensity level
        """
        return Panel(
            elements=[
                self._get_text_element(self.text_manager.get_text(IntensityDefinitionTexts.ANNOYING_DEFINITION)),
                self._get_text_element(self.text_manager.get_text(IntensityDefinitionTexts.HURTFUL_DEFINITION)),
                self._get_text_element(self.text_manager.get_text(IntensityDefinitionTexts.DISABLING_DEFINITION)),
                self._get_text_element(self.text_manager.get_text(IntensityDefinitionTexts.EXCRUCIATING_DEFINITION)),
            ],
            level="info",
            title_element=TitleElement(
                grade="c",
                title=self.text_manager.get_text(IntensityDefinitionTexts.PANEL_TITLE),
                type="grade",
            ),
            topics=["suffering-footprint"],
        )

    def _get_animal_pain_for_panel(self, animal_type: AnimalType, pain_type: PainType) -> Element | None:
        """
        Create a text element with pain information for a specific animal and pain type.

        Args:
            animal_type: The animal type to filter for
            pain_type: The type of pain to display (physical or psychological)

        Returns:
            A text element with the formatted HTML, or None if the animal has no data
        """
        # Find the animal in the pain report
        animal_data = next((animal for animal in self.pain_report.animals if animal.animal_type == animal_type), None)

        if not animal_data:
            return None

        # Generate HTML for this animal
        animal_html = self._generate_animal_pain_html(animal_pain_report=animal_data, pain_type=pain_type)

        # Return the text element
        return self._get_text_element(animal_html)

    def _create_physical_pain_panel(self) -> Panel:
        """
        Create a panel displaying physical pain information by animal type.

        Returns:
            A panel with physical pain information organized by animal
        """
        elements = [
            self._get_text_element(self.text_manager.get_text(PhysicalPainTexts.DEFINITION)),
            self._get_text_element(self.text_manager.get_text(PhysicalPainTexts.DURATION_EXPLANATION)),
        ]

        # Add each animal from the pain report
        for animal in self.pain_report.animals:
            animal_element = self._get_animal_pain_for_panel(animal.animal_type, PainType.PHYSICAL)
            if animal_element:
                elements.append(animal_element)

        # Add footer
        elements.append(self._get_text_element(self.text_manager.get_text(PhysicalPainTexts.MORE_DETAILS)))

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                grade="c",
                name="physical-pain",
                title=self.text_manager.get_text(PhysicalPainTexts.PANEL_TITLE),
                type="grade",
            ),
            topics=["suffering-footprint"],
        )

    def _create_psychological_pain_panel(self) -> Panel:
        """
        Create a panel displaying psychological pain information by animal type.
        """
        elements = [
            self._get_text_element(self.text_manager.get_text(PsychologicalPainTexts.DEFINITION)),
            self._get_text_element(self.text_manager.get_text(PsychologicalPainTexts.DURATION_EXPLANATION)),
        ]

        # Add each animal from the pain report
        for animal in self.pain_report.animals:
            animal_element = self._get_animal_pain_for_panel(animal.animal_type, PainType.PSYCHOLOGICAL)
            if animal_element:
                elements.append(animal_element)

        # Add footer
        elements.append(self._get_text_element(self.text_manager.get_text(PsychologicalPainTexts.MORE_DETAILS)))

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                grade="c",
                name="psychological-pain",
                title=self.text_manager.get_text(PsychologicalPainTexts.PANEL_TITLE),
                type="grade",
            ),
            topics=["suffering-footprint"],
        )

    def _get_text_element(self, text: str) -> Element:
        """
        Create a text element with HTML content for use in a panel.

        Args:
            text: The HTML content as a string

        Returns:
            An Element object with the text content properly wrapped
        """
        return Element(element_type="text", text_element=TextElement(html=text))

    def _get_breeding_type_and_quantity_html(
        self, animal_type: AnimalType, breeding_type_and_quantity: BreedingTypeAndQuantity
    ) -> str:
        """
        Format animal type, breeding type and product quantity information as HTML.
        """
        breeding_type = breeding_type_and_quantity.breeding_type
        quantity = breeding_type_and_quantity.quantity

        return self.text_manager.format_text(
            AnimalInfoTexts.ANIMAL_INFO_TEMPLATE,
            animal_name=animal_type.translated_name(self._),
            breeding_type=breeding_type.translated_name(self._)
            if breeding_type
            else self.text_manager.get_text(AnimalInfoTexts.NOT_FOUND),
            quantity=str(int(quantity)) + self.text_manager.get_text(AnimalInfoTexts.UNIT)
            if quantity is not None
            else self.text_manager.get_text(AnimalInfoTexts.NOT_FOUND),
        )

    def _format_duration(self, seconds: int) -> str:
        """
        Format a duration in seconds into a human-readable string.
        """
        if seconds <= 0:
            return self.text_manager.get_text(DurationTexts.ZERO_SECOND)

        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
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

    def _generate_animal_pain_html(self, animal_pain_report: AnimalPainReport, pain_type: PainType) -> str:
        """
        Generate HTML for a single animal's pain levels of a specific type.

        Args:
            animal_pain_report: The animal pain report containing all pain data
            pain_type: Type of pain to filter by (physical or psychological)

        Returns:
            HTML string for this animal's pain levels
        """
        # Get the pain levels for this pain_type for this animal (sorted by intensity)
        pain_levels = animal_pain_report.get_pain_levels_by_type(pain_type)

        # If no pain of this type, return empty string
        if not pain_levels:
            return ""

        # Start with animal name and breeding type
        animal_type = animal_pain_report.animal_type
        breeding_type = animal_pain_report.breeding_type_and_quantity.breeding_type
        if not breeding_type:
            raise ValueError("Missing breeding type while generating HTML for animal pain report")
        html_parts = [f"<b>{animal_type.translated_name(self._)} - {breeding_type.translated_name(self._)}</b>"]

        # Add pain levels in standardized order
        html_parts.append("<ul>")
        for pain_level_data in pain_levels:
            intensity_label = pain_level_data.pain_intensity.translated_name(self._)
            duration = self._format_duration(pain_level_data.seconds_in_pain)

            html_parts.append(f"<li><b>{intensity_label}</b> : {duration}</li>")
        html_parts.append("</ul>")

        return "".join(html_parts)
