import logging

import httpx
from pydantic import HttpUrl, ValidationError

from app.business.open_food_facts.pain_report_calculator import PainReportCalculator
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import (
    AnimalType,
    LayingHenBreedingType,
)
from app.schemas.open_food_facts.external import ProductData, ProductResponse
from app.schemas.open_food_facts.internal import (
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


def get_knowledge_panel_response(pain_report: PainReport) -> KnowledgePanelResponse:
    return KnowledgePanelResponse(
        panels={
            "main": create_main_panel(pain_report),
            "intensities_definitions": create_intensities_definitions_panel(),
            "physical_pain": create_physical_pain_panel(pain_report),
            "psychological_pain": create_psychological_pain_panel(pain_report)
        }
    )


def create_main_panel(pain_report: PainReport) -> Panel:
    elements = [
        get_text_element((
            "L'<a href=\"https://empreinte-souffrance.org/\">empreinte Souffrance</a> "
            "est calculée à partir des travaux de recherche du <a href=\"https://welfarefootprint.org/\">"
            "Welfare Footprint Institute</a>."
        )),
        get_text_element((
            "Le score et les détails exposés ci-dessous sont basés sur les données suivantes "
            "(renseignées par la communauté d'Open Food Facts):"
        ))]

    for breeding_type_with_weight in pain_report.breeding_types_with_weights:
        elements.append(get_text_element(text=generate_breeding_type_html(breeding_type_with_weight)))

    elements.extend([
        Element(element_type="panel", panel_element=PanelElement(panel_id="intensities_definitions")),
        Element(element_type="panel", panel_element=PanelElement(panel_id="physical_pain")),
        Element(element_type="panel", panel_element=PanelElement(panel_id="psychological_pain")),
    ])

    return Panel(
        elements=elements,
        level="info",
        title_element=TitleElement(
            grade="c",
            icon_url=HttpUrl("https://iili.io/3o05WOX.png"),
            name="suffering-footprint",
            subtitle="Qu’est-ce que l’empreinte souffrance ?",
            title="Empreinte souffrance",
            type="grade"
        ),
        topics=["suffering-footprint"]
    )


def create_intensities_definitions_panel() -> Panel:
    return Panel(
        elements=[
            get_text_element((
                "<b>Inconfort</b> : Désagrément perceptible mais pouvant être ignoré. "
                "N'interfère pas avec les activités quotidiennes ou les comportements motivés "
                "(exploration, confort, entretien). Absence d'expressions visibles de douleur "
                "et de perturbations physiologiques."
            )),
            get_text_element((
                "<b>Douleur</b> : Douleur persistante avec possibilité de brefs moments d'oubli lors de "
                "distractions. Réduit la fréquence des comportements motivés et altère partiellement les "
                "capacités fonctionnelles, tout en permettant la réalisation des activités essentielles."
            )),
            get_text_element((
                "<b>Souffrance</b> : Douleur constante qui prend priorité sur la plupart des comportements. "
                "Empêche le bien-être positif et modifie drastiquement le niveau d'activité. "
                "Requiert des analgésiques plus puissants et provoque une inattention à l'environnement."
            )),
            get_text_element((
                "<b>Agonie</b> : Douleur extrême intolérable, même brièvement. "
                "Chez les humains, marquerait le seuil de souffrance sous lequel beaucoup de personnes choisissent "
                "de mettre fin à leurs jours plutôt que de l'endurer. Déclenche des manifestations involontaires "
                "(cris, tremblements, agitation extrême) et ne peut être soulagée."
            )),
        ],
        level="info",
        title_element=TitleElement(
            grade="c",
            subtitle="Mieux comprendre les intensités de souffrance",
            title="Définitions des niveaux d'intensité",
            type="grade"
        ),
        topics=["suffering-footprint"]
    )


def create_physical_pain_panel(pain_report) -> Panel:
    return Panel(
        elements=[
            get_text_element((
                "Vous pouvez retrouver le détail (fractures, plaies...) "
                "<a href=\"https://empreinte-souffrance.org/\">sur notre site</a>."
            )),
            get_text_element(_generate_html_items_for_pain_report(pain_report))
        ],
        level="info",
        title_element=TitleElement(
            grade="c",
            name="physical-pain",
            title="Douleur physique",
            type="grade"
        ),
        topics=["suffering-footprint"]
    )


def create_psychological_pain_panel(pain_report) -> Panel:
    return Panel(
        elements=[
            get_text_element((
                "Vous pouvez retrouver le détail (Impossibilité de couver...) "
                "<a href=\"https://empreinte-souffrance.org/\">sur notre site</a>."
            )),
            get_text_element(_generate_html_items_for_pain_report(pain_report))
        ],
        level="info",
        title_element=TitleElement(
            grade="c",
            name="psychological-pain",
            title="Douleur psychologique",
            type="grade"
        ),
        topics=["suffering-footprint"]
    )


def get_text_element(text: str) -> Element:
    return Element(element_type="text", text_element=TextElement(html=text))


def get_breeding_type_mapping() -> dict:
    return {
        LayingHenBreedingType.CONVENTIONAL_CAGE: "Cage conventionnelle",
        LayingHenBreedingType.FURNISHED_CAGE: "Cage améliorée",
        LayingHenBreedingType.BARN: "Au sol",
        LayingHenBreedingType.FREE_RANGE: "En plein air"
    }


def get_animal_type_mapping() -> dict:
    return {
        AnimalType.LAYING_HEN: "Poule pondeuse",
        AnimalType.BROILER_CHICKEN: "Poulet de chair"
    }


def generate_breeding_type_html(breeding_type_with_weight: BreedingTypeAndWeight) -> str:
    breeding_type_mapping = get_breeding_type_mapping()
    animal_type_mapping = get_animal_type_mapping()
    return (
        f"<b>{animal_type_mapping[breeding_type_with_weight.animal_type]} :</b>\n"
        f"<ul><li>Type d’élevage : <b>{breeding_type_mapping[breeding_type_with_weight.breeding_type]}</b></li>\n"
        f"<li>Quantité d’oeuf dans le produit : <b>{breeding_type_with_weight.animal_product_weight}g</b></li></ul>"
    )


def _format_duration(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    parts = []
    if days:
        parts.append(f"{days} jours")
    if hours:
        parts.append(f"{hours} heures")
    if minutes:
        parts.append(f"{minutes} minutes")
    if sec:
        parts.append(f"{sec} secondes")
    return " ".join(parts)


def _generate_html_items_for_pain_report(pain_report: PainReport) -> str:
    pain_labels = {
        "EXCRUCIATING": "Agonie",
        "DISABLING": "Souffrance",
        "HURTFUL": "Douleur",
        "ANNOYING": "Inconfort"
    }

    pain_durations = {
        category.pain_intensity.name: sum(animal.seconds_in_pain for animal in category.animals)
        for category in pain_report.pain_categories
    }

    html = "<ul>" + "".join(
        f"<li><b>{pain_labels.get(pain_intensity, pain_intensity)}</b> : {_format_duration(duration)}</li>"
        for pain_intensity, duration in sorted(pain_durations.items(), key=lambda x: x[1], reverse=True)
    ) + "</ul>"

    return html
