import logging
from typing import Callable

import httpx
from pydantic import HttpUrl, ValidationError

from app.business.open_food_facts.pain_report_calculator import PainReportCalculator
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import AnimalType, PainType
from app.schemas.open_food_facts.external import ProductData, ProductResponse
from app.schemas.open_food_facts.internal import (
    AnimalPainReport,
    BreedingTypeAndWeight,
    Element,
    KnowledgePanelResponse,
    PainReport,
    Panel,
    PanelElement,
    TextElement,
    TitleElement,
)

logger = logging.getLogger("app")


async def get_data_from_off(barcode: str) -> ProductData:
    """
    Retrieve useful product data from OFF to compute the breeding type and the weight of animal product
    We actually use the OFF Search-a-licious API.
    If an error occurs, we raise a ResourceNotFoundException to return a clean response to OFF

    Args:
        barcode: The product barcode
    Returns:
        A ProductData containing the categories and labels tags
    Raises:
        ResourceNotFoundException: If the product cannot be found or data validation fails
    """
    url = "https://search.openfoodfacts.org/search"
    tags = ["categories_tags", "labels_tags"]
    params = {"q": f"code:{barcode}", "fields": ",".join(tags)}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
    except Exception as e:
        logger.warning(f"Can't get product data from OFF API: {barcode}")
        raise ResourceNotFoundException(f"Can't get product data from OFF API: {barcode}") from e

    try:
        product_response = ProductResponse.model_validate(response.json())
    except ValidationError as e:
        logger.error(f"Failed to validate product data: {e}")
        raise ResourceNotFoundException(f"Failed to validate product data retrieved from OFF: {barcode}") from e

    if not product_response.hits:
        logger.warning(f"No hits found for params: {params}")
        raise ResourceNotFoundException(f"No hits returned by OFF API: {barcode}")

    product_data = product_response.hits[0]
    return product_data


async def compute_suffering_footprint(barcode: str) -> PainReport:
    """
    Compute the suffering footprint for a product based on its barcode.

    Args:
        barcode: The product barcode

    Returns:
        PainReport if applicable, None otherwise
    """
    # Get the product data
    product_data = await get_data_from_off(barcode)

    # Create calculator with the retrieved data
    calculator = PainReportCalculator(product_data)

    # Generate and return the pain report
    return calculator.get_pain_report()


def get_knowledge_panel_response(pain_report: PainReport, translator: Callable) -> KnowledgePanelResponse:
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

    def __init__(self, pain_report: PainReport, translator: Callable):
        """
        Initialize the generator with a pain report and translator.

        Args:
            pain_report: The pain report containing animal data and pain durations
            translator: The translation function to use for i18n
        """
        self.pain_report = pain_report
        self._ = translator

    def get_response(self) -> KnowledgePanelResponse:
        """
        Create a complete knowledge panel response with all suffering footprint panels.

        Returns:
            A complete KnowledgePanelResponse with all necessary panels
        """
        return KnowledgePanelResponse(
            panels={
                "main": self.create_main_panel(),
                "intensities_definitions": self.create_intensities_definitions_panel(),
                "physical_pain": self.create_physical_pain_panel(),
                "psychological_pain": self.create_psychological_pain_panel(),
            }
        )

    def create_main_panel(self) -> Panel:
        """
        Create the main panel showing general information about the suffering footprint.

        This panel includes an explanation of the suffering footprint, the breeding
        type and animal product weight information, and links to the other panels.

        Returns:
            A panel with general information and links to detailed panels
        """
        elements = [
            self._get_text_element(
                self._(
                    "The <a href='https://empreinte-souffrance.org/'>Suffering Footprint</a> is calculated based "
                    "on research from the <a href='https://welfarefootprint.org/'>Welfare Footprint Institute</a>."
                )
            ),
            self._get_text_element(
                self._(
                    "The score and details shown below are based on the following data "
                    "(provided by the Open Food Facts community)"
                )
            ),
        ]

        for animal in self.pain_report.animals:
            elements.append(
                self._get_text_element(
                    self._get_breeding_type_and_weight_html(animal.animal_type, animal.breeding_type_with_weight)
                )
            )

        elements.extend(
            [
                Element(element_type="panel", panel_element=PanelElement(panel_id="intensities_definitions")),
                Element(element_type="panel", panel_element=PanelElement(panel_id="physical_pain")),
                Element(element_type="panel", panel_element=PanelElement(panel_id="psychological_pain")),
            ]
        )

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                grade="c",
                icon_url=HttpUrl("https://iili.io/3o05WOX.png"),
                name="suffering-footprint",
                subtitle=self._("What is the suffering footprint?"),
                title=self._("Suffering footprint"),
                type="grade",
            ),
            topics=["suffering-footprint"],
        )

    def create_intensities_definitions_panel(self) -> Panel:
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
                self._get_text_element(
                    self._(
                        "<b>Excruciating</b>: Extreme unbearable pain, even briefly. "
                        "In humans, this would mark the threshold of suffering below which many people "
                        "choose to end their lives rather than endure it. Triggers involuntary manifestations "
                        "(screams, tremors, extreme agitation) and cannot be relieved."
                    )
                ),
                self._get_text_element(
                    self._(
                        "<b>Disabling</b>: Constant pain that takes priority over most behaviors. "
                        "Prevents positive well-being and drastically alters activity level. "
                        "Requires stronger painkillers and causes inattention to the environment."
                    )
                ),
                self._get_text_element(
                    self._(
                        "<b>Hurtful</b>: Persistent pain with the possibility of brief moments of forgetting during "
                        "distractions. Reduces the frequency of motivated behaviors and partially alters functional "
                        "capabilities, while allowing essential activities to be carried out."
                    )
                ),
                self._get_text_element(
                    self._(
                        "<b>Annoying</b>: Noticeable discomfort that can be ignored. Does not interfere with daily "
                        "activities or motivated behaviors (exploration, comfort, maintenance). "
                        "No visible expressions of pain or physiological disturbances."
                    )
                ),
            ],
            level="info",
            title_element=TitleElement(
                grade="c",
                subtitle=self._("Better understand suffering intensities"),
                title=self._("Intensity level definitions"),
                type="grade",
            ),
            topics=["suffering-footprint"],
        )

    def get_animal_pain_for_panel(self, animal_type: AnimalType, pain_type: PainType) -> Element | None:
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

    def create_physical_pain_panel(self) -> Panel:
        """
        Create a panel displaying physical pain information by animal type.

        Returns:
            A panel with physical pain information organized by animal
        """
        elements = [
            self._get_text_element(
                self._(
                    "<b>Physical pain</b> includes all bodily suffering experienced by animals: "
                    "fractures, wounds, diseases, breathing difficulties, etc."
                )
            ),
            self._get_text_element(
                self._(
                    "The durations below represent the suffering time caused "
                    "by the production of animal-derived ingredients in this product:"
                )
            ),
        ]

        # Add each animal from the pain report
        for animal in self.pain_report.animals:
            animal_element = self.get_animal_pain_for_panel(animal.animal_type, PainType.PHYSICAL)
            if animal_element:
                elements.append(animal_element)

        # Add footer
        elements.append(
            self._get_text_element(
                self._(
                    "You can find more details about the different types of physical suffering "
                    "<a href='https://empreinte-souffrance.org/'>on our website</a>."
                )
            )
        )

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(grade="c", name="physical-pain", title=self._("Physical pain"), type="grade"),
            topics=["suffering-footprint"],
        )

    def create_psychological_pain_panel(self) -> Panel:
        """
        Create a panel displaying psychological pain information by animal type.

        Returns:
            A panel with psychological pain information organized by animal
        """
        elements = [
            self._get_text_element(
                self._(
                    "<b>Psychological pain</b> includes mental suffering experienced by animals: "
                    "stress, anxiety, inability to express natural behaviors, etc."
                )
            ),
            self._get_text_element(
                self._(
                    "The durations below represent the suffering time caused "
                    "by the production of animal-derived ingredients in this product:"
                )
            ),
        ]

        # Add each animal from the pain report
        for animal in self.pain_report.animals:
            animal_element = self.get_animal_pain_for_panel(animal.animal_type, PainType.PSYCHOLOGICAL)
            if animal_element:
                elements.append(animal_element)

        # Add footer
        elements.append(
            self._get_text_element(
                self._(
                    "You can find more details about the different types of psychological suffering "
                    "<a href='https://empreinte-souffrance.org/'>on our website</a>."
                )
            )
        )

        return Panel(
            elements=elements,
            level="info",
            title_element=TitleElement(
                grade="c", name="psychological-pain", title=self._("Psychological pain"), type="grade"
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

    def _get_breeding_type_and_weight_html(
        self, animal_type: AnimalType, breeding_type_with_weight: BreedingTypeAndWeight
    ) -> str:
        """
        Format animal type, breeding type and product weight information as HTML.

        Creates a formatted HTML string showing the animal type (e.g., "Poule pondeuse"),
        the breeding type (e.g., "Cage conventionnelle"), and the weight of animal product
        in the food item.

        Args:
            animal_type: The type of animal (e.g., LAYING_HEN)
            breeding_type_with_weight: Object containing the breeding type and weight data

        Returns:
            Formatted HTML string with animal information
        """
        html_template = self._(
            "<b>{animal_name} :</b><ul>"
            "<li>Breeding type: <b>{breeding_type}</b></li>"
            "<li>Quantity of egg in the product: <b>{weight}g</b></li></ul>"
        )
        return html_template.format(
            animal_name=animal_type.translated_name(self._),
            breeding_type=breeding_type_with_weight.breeding_type.translated_name(self._),
            weight=breeding_type_with_weight.animal_product_weight,
        )

    def _format_duration(self, seconds: int) -> str:
        """
        Format a duration in seconds into a human-readable string.

        Converts seconds into a combination of days, hours, minutes and seconds
        as appropriate.

        Args:
            seconds: The duration in seconds to format

        Returns:
            A formatted string like "2 days 5 hours 30 minutes 10 seconds"
        """
        if seconds <= 0:
            return self._("0 second")

        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        parts = []
        if days:
            parts.append(self._("{} days").format(days))
        if hours:
            parts.append(self._("{} hours").format(hours))
        if minutes:
            parts.append(self._("{} minutes").format(minutes))
        if sec:
            parts.append(self._("{} seconds").format(sec))
        return " ".join(parts) if parts else self._("0 second")

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
        breeding_type = animal_pain_report.breeding_type_with_weight.breeding_type
        html_parts = [f"<b>{animal_type.translated_name(self._)} - {breeding_type.translated_name(self._)}</b>"]

        # Add pain levels in standardized order
        html_parts.append("<ul>")
        for pain_level_data in pain_levels:
            intensity_label = pain_level_data.pain_intensity.translated_name(self._)
            duration = self._format_duration(pain_level_data.seconds_in_pain)

            html_parts.append(f"<li><b>{intensity_label}</b> : {duration}</li>")
        html_parts.append("</ul>")

        return "".join(html_parts)
