from typing import List

from pydantic import BaseModel

from app.enums.open_food_facts.enums import AnimalType, BroilerChickenBreedingType, LayingHenBreedingType, PainType


class AnimalBreedingType(BaseModel):
    laying_hen_breeding_type: LayingHenBreedingType | None = None
    broiler_chicken_breeding_type: BroilerChickenBreedingType | None = None


class AnimalProductWeight(BaseModel):
    egg_weight: int | None = None
    chicken_weight: int | None = None


class AnimalPainDuration(BaseModel):
    animal_type: AnimalType
    seconds_in_pain: int


class PainCategory(BaseModel):
    pain_type: PainType
    animals: List[AnimalPainDuration]


class PainReport(BaseModel):
    pain_categories: List[PainCategory]


class KnowledgePanelResponse(BaseModel):
    """
    Response model for knowledge panel endpoint.
    """

    global_score: float
    pain_report: PainReport
