from enum import StrEnum, auto

LAYING_HEN_FURNISHED_CAGE_TAGS = ["en:cage-chicken-eggs"]


class AnimalType(StrEnum):
    LAYING_HEN = auto()
    BROILER_CHICKEN = auto()

class LayingHenBreedingType(StrEnum):
    CONVENTIONAL_CAGE = auto()
    FURNISHED_CAGE = auto()
    BARN = auto()
    FREE_RANGE = auto()

class BroilerChickenBreedingType(StrEnum):
    FREE_RANGE = auto()


class PainType(StrEnum):
    EXCRUCIATING = auto()
    DISABLING = auto()
    HURTFUL = auto()
    ANNOYING = auto()


LAYING_HEN_PAIN_FOR_100G = {
    LayingHenBreedingType.FURNISHED_CAGE: {
        PainType.EXCRUCIATING: 100,
        PainType.DISABLING: 2000,
        PainType.HURTFUL: 3000,
        PainType.ANNOYING: 4000
    },
}
