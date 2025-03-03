from enum import StrEnum, auto
from typing import List

from pydantic import BaseModel


class AnimalType(StrEnum):
    LAYING_HEN = auto()


class PainType(StrEnum):
    EXCRUCIATING = auto()
    DISABLING = auto()
    HURTFUL = auto()
    ANNOYING = auto()


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

    logo_url: str | None = None
    global_score: float
    pain_info: PainReport


PAIN_REPORT_EXAMPLE = PainReport(
    pain_categories=[
        PainCategory(
            pain_type=PainType.EXCRUCIATING,
            animals=[
                AnimalPainDuration(
                    animal_type=AnimalType.LAYING_HEN,
                    seconds_in_pain=3600
                )
            ]
        ),
        PainCategory(
            pain_type=PainType.DISABLING,
            animals=[
                AnimalPainDuration(
                    animal_type=AnimalType.LAYING_HEN,
                    seconds_in_pain=7200
                )
            ]
        ),
        PainCategory(
            pain_type=PainType.HURTFUL,
            animals=[
                AnimalPainDuration(
                    animal_type=AnimalType.LAYING_HEN,
                    seconds_in_pain=1800
                )
            ]
        ),
        PainCategory(
            pain_type=PainType.ANNOYING,
            animals=[
                AnimalPainDuration(
                    animal_type=AnimalType.LAYING_HEN,
                    seconds_in_pain=600
                )
            ]
        ),
    ]
)

