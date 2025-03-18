from typing import List

from pydantic import BaseModel

from app.enums.open_food_facts.enums import AnimalType, BroilerChickenBreedingType, LayingHenBreedingType, PainType


class BreedingTypeAndWeight(BaseModel):
    animal_type: AnimalType
    breeding_type: LayingHenBreedingType | BroilerChickenBreedingType
    animal_product_weight: int = 0  # in grams


class AnimalPainDuration(BaseModel):
    animal_type: AnimalType
    seconds_in_pain: int


class PainCategory(BaseModel):
    pain_type: PainType
    animals: List[AnimalPainDuration]


class PainReport(BaseModel):
    pain_categories: List[PainCategory]
    breeding_types_with_weights: List[BreedingTypeAndWeight]


class KnowledgePanelResponse(BaseModel):
    """
    Response model for knowledge panel endpoint.
    """
    pain_report: PainReport
