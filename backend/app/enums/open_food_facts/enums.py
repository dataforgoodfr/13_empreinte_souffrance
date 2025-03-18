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


class PainIntensity(StrEnum):
    EXCRUCIATING = auto()
    DISABLING = auto()
    HURTFUL = auto()
    ANNOYING = auto()


class PainType(StrEnum):
    PHYSICAL = auto()
    PSYCHOLOGICAL = auto()


# Time in pain by animal type, per 100g, in seconds
TIME_IN_PAIN_FOR_100G_IN_SECONDS = {
    AnimalType.LAYING_HEN: {
        LayingHenBreedingType.CONVENTIONAL_CAGE: {
            PainIntensity.EXCRUCIATING: 100,
            PainIntensity.DISABLING: 2000,
            PainIntensity.HURTFUL: 3000,
            PainIntensity.ANNOYING: 4000
        },
        LayingHenBreedingType.FURNISHED_CAGE: {
            PainIntensity.EXCRUCIATING: 100,
            PainIntensity.DISABLING: 2000,
            PainIntensity.HURTFUL: 3000,
            PainIntensity.ANNOYING: 4000
        },
        LayingHenBreedingType.BARN: {
            PainIntensity.EXCRUCIATING: 100,
            PainIntensity.DISABLING: 2000,
            PainIntensity.HURTFUL: 3000,
            PainIntensity.ANNOYING: 4000
        },
        LayingHenBreedingType.FREE_RANGE: {
            PainIntensity.EXCRUCIATING: 0,
            PainIntensity.DISABLING: 111,
            PainIntensity.HURTFUL: 2222,
            PainIntensity.ANNOYING: 33333
        },
    },
    AnimalType.BROILER_CHICKEN: {
        BroilerChickenBreedingType.FREE_RANGE: {
            PainIntensity.EXCRUCIATING: 120,
            PainIntensity.DISABLING: 4500,
            PainIntensity.HURTFUL: 8000,
            PainIntensity.ANNOYING: 35000
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
    AnimalType.BROILER_CHICKEN: {
        # Can be tested with this barcode: 3256229237063
        # BroilerChickenBreedingType.FREE_RANGE: ["en:cooked-chicken-breast-slices"]
    },
}
