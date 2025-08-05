from typing import Dict, List

from pydantic import BaseModel, HttpUrl

from app.enums.open_food_facts.enums import (
    AnimalType,
    BreedingType,
    PainIntensity,
    PainType,
)


class ProductType(BaseModel):
    is_mixed: bool
    animal_types: set[AnimalType]


# Pain report models, used for calculation
class BreedingTypeAndQuantity(BaseModel):
    breeding_type: BreedingType | None = None
    quantity: float | None = None  # in grams


class PainLevelData(BaseModel):
    pain_intensity: PainIntensity
    pain_type: PainType
    seconds_in_pain: int


class AnimalPainReport(BaseModel):
    animal_type: AnimalType
    pain_levels: List[PainLevelData] = []
    breeding_type_and_quantity: BreedingTypeAndQuantity

    def get_pain_levels_by_type(self, pain_type: PainType) -> List[PainLevelData]:
        """Returns the PainLevelData objects for a specific pain type, sorted by intensity"""
        pain_levels_by_type = [pain_level for pain_level in self.pain_levels if pain_level.pain_type is pain_type]

        # Sort by intensity order using the class method
        return sorted(
            pain_levels_by_type, key=lambda pain: PainIntensity.get_intensity_order().index(pain.pain_intensity)
        )


class PainReport(BaseModel):
    animals: List[AnimalPainReport] = []
    product_name: str | None
    product_image_url: HttpUrl | None = None


# Knowledge panel response models
class TextElement(BaseModel):
    html: str


class PanelElement(BaseModel):
    panel_id: str


class Element(BaseModel):
    element_type: str
    text_element: TextElement | None = None
    panel_element: PanelElement | None = None


class TitleElement(BaseModel):
    title: str
    subtitle: str | None = None
    name: str | None = None
    icon_url: HttpUrl | None = None


class Panel(BaseModel):
    elements: List[Element]
    level: str
    title_element: TitleElement
    topics: List[str]


class ProductInfo(BaseModel):
    image_url: HttpUrl | None
    name: str | None


class KnowledgePanelResponse(BaseModel):
    """
    Response model for knowledge panel endpoint.
    """

    panels: Dict[str, Panel]
    product: ProductInfo
