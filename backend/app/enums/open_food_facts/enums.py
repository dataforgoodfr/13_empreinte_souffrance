from enum import StrEnum, auto


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


# Time in pain by animal type, per 100g, in seconds
TIME_IN_PAIN_FOR_100G_IN_SECONDS = {
    AnimalType.LAYING_HEN: {
        LayingHenBreedingType.CONVENTIONAL_CAGE: {
            PainType.EXCRUCIATING: 100,
            PainType.DISABLING: 2000,
            PainType.HURTFUL: 3000,
            PainType.ANNOYING: 4000
        },
        LayingHenBreedingType.FURNISHED_CAGE: {
            PainType.EXCRUCIATING: 100,
            PainType.DISABLING: 2000,
            PainType.HURTFUL: 3000,
            PainType.ANNOYING: 4000
        },
        LayingHenBreedingType.BARN: {
            PainType.EXCRUCIATING: 100,
            PainType.DISABLING: 2000,
            PainType.HURTFUL: 3000,
            PainType.ANNOYING: 4000
        },
        LayingHenBreedingType.FREE_RANGE: {
            PainType.EXCRUCIATING: 0,
            PainType.DISABLING: 111,
            PainType.HURTFUL: 2222,
            PainType.ANNOYING: 33333
        },
    },
    AnimalType.BROILER_CHICKEN: {
        BroilerChickenBreedingType.FREE_RANGE: {
            PainType.EXCRUCIATING: 120,
            PainType.DISABLING: 4500,
            PainType.HURTFUL: 8000,
            PainType.ANNOYING: 35000
        },
    }
    # Here will come data for other animals...
}


TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE = {
    AnimalType.LAYING_HEN: {
        LayingHenBreedingType.CONVENTIONAL_CAGE: [],
        LayingHenBreedingType.FURNISHED_CAGE: ["en:cage-chicken-eggs"],
        LayingHenBreedingType.BARN: ["en:barn-chicken-eggs"],
        LayingHenBreedingType.FREE_RANGE: ["en:free-range-chicken-eggs", "en:organic-eggs"],
    },
    AnimalType.BROILER_CHICKEN: {},
}
