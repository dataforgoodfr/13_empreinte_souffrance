from typing import Dict, List

from pydantic import BaseModel, HttpUrl

from app.enums.open_food_facts.enums import AnimalType, BroilerChickenBreedingType, LayingHenBreedingType, PainIntensity


# Pain report models, used for calculation
class BreedingTypeAndWeight(BaseModel):
    animal_type: AnimalType
    breeding_type: LayingHenBreedingType | BroilerChickenBreedingType
    animal_product_weight: int = 0  # in grams


class AnimalPainDuration(BaseModel):
    animal_type: AnimalType
    seconds_in_pain: int


class PainCategory(BaseModel):
    pain_intensity: PainIntensity
    animals: List[AnimalPainDuration]


class PainReport(BaseModel):
    pain_categories: List[PainCategory]
    breeding_types_with_weights: List[BreedingTypeAndWeight]


# Knowledge panel response models
class TextElement(BaseModel):
    html: str


class PanelElement(BaseModel):
    panel_id: str


class Element(BaseModel):
    element_type: str
    text_element: TextElement | None  = None
    panel_element: PanelElement | None = None


class TitleElement(BaseModel):
    grade: str
    title: str
    type: str
    subtitle: str | None = None
    name: str | None = None
    icon_url: HttpUrl | None = None


class Panel(BaseModel):
    elements: List[Element]
    level: str
    title_element: TitleElement
    topics: List[str]


class KnowledgePanelResponse(BaseModel):
    """
    Response model for knowledge panel endpoint.
    """
    panels: Dict[str, Panel]
