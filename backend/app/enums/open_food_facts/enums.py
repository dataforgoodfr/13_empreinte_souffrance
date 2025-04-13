from collections.abc import Callable
from enum import StrEnum, auto


class AnimalType(StrEnum):
    LAYING_HEN = auto()
    BROILER_CHICKEN = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this animal type"""
        mappings = {"laying_hen": _("Laying hen"), "broiler_chicken": _("Broiler chicken")}
        return mappings.get(self.value, self.value)


class LayingHenBreedingType(StrEnum):
    CAGE = auto()
    CONVENTIONAL_CAGE = auto()
    FURNISHED_CAGE = auto()
    BARN = auto()
    FREE_RANGE = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this breeding type"""
        mappings = {
            "cage": _("Cage"),
            "conventional_cage": _("Conventional cage"),
            "furnished_cage": _("Furnished cage"),
            "barn": _("Barn"),
            "free_range": _("Free range"),
        }
        return mappings.get(self.value, self.value)

    def get_more_specific_breeding_from_country(self, countries: list[str] | None):
        """Return the type of cage breeding depending on the sales country"""
        breeding_type = self
        if breeding_type == LayingHenBreedingType.CAGE:
            if countries and any(country in COUNTRIES_WHERE_CAGES_ARE_FURNISHED for country in countries):
                breeding_type = LayingHenBreedingType.FURNISHED_CAGE
            else:
                breeding_type = LayingHenBreedingType.CONVENTIONAL_CAGE
        return breeding_type


class BroilerChickenBreedingType(StrEnum):
    FREE_RANGE = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this breeding type"""
        mappings = {"free_range": _("Free range")}
        return mappings.get(self.value, self.value)

    def get_more_specific_breeding_from_country(self, countries: list[str] | None):
        """Return the type of cage breeding depending on the sales country"""
        return self


class PainIntensity(StrEnum):
    EXCRUCIATING = auto()
    DISABLING = auto()
    HURTFUL = auto()
    ANNOYING = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this pain intensity"""
        mappings = {
            "excruciating": _("Excruciating"),
            "disabling": _("Disabling"),
            "hurtful": _("Hurtful"),
            "annoying": _("Annoying"),
        }
        return mappings.get(self.value, self.value)

    @classmethod
    def get_intensity_order(cls) -> list["PainIntensity"]:
        """Return the order of pain intensities from most to least severe."""
        return [cls.ANNOYING, cls.HURTFUL, cls.DISABLING, cls.EXCRUCIATING]


class PainType(StrEnum):
    PHYSICAL = auto()
    PSYCHOLOGICAL = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this pain type"""
        mappings = {"physical": _("Physical"), "psychological": _("Psychological")}
        return mappings.get(self.value, self.value)


# Time in pain by animal type, per 100g, in seconds, separated by pain type
TIME_IN_PAIN_FOR_100G_IN_SECONDS = {
    AnimalType.LAYING_HEN: {
        LayingHenBreedingType.CONVENTIONAL_CAGE: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 70,
                PainIntensity.DISABLING: 1200,
                PainIntensity.HURTFUL: 1800,
                PainIntensity.ANNOYING: 2400,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 30,
                PainIntensity.DISABLING: 800,
                PainIntensity.HURTFUL: 1200,
                PainIntensity.ANNOYING: 1600,
            },
        },
        LayingHenBreedingType.FURNISHED_CAGE: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 0,
                PainIntensity.DISABLING: 1100,
                PainIntensity.HURTFUL: 1700,
                PainIntensity.ANNOYING: 2300,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 40,
                PainIntensity.DISABLING: 900,
                PainIntensity.HURTFUL: 1300,
                PainIntensity.ANNOYING: 1700,
            },
        },
        LayingHenBreedingType.BARN: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 50,
                PainIntensity.DISABLING: 1000,
                PainIntensity.HURTFUL: 1500,
                PainIntensity.ANNOYING: 2000,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 50,
                PainIntensity.DISABLING: 1000,
                PainIntensity.HURTFUL: 1500,
                PainIntensity.ANNOYING: 2000,
            },
        },
        LayingHenBreedingType.FREE_RANGE: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 0,
                PainIntensity.DISABLING: 60,
                PainIntensity.HURTFUL: 1000,
                PainIntensity.ANNOYING: 16000,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 1,
                PainIntensity.DISABLING: 51,
                PainIntensity.HURTFUL: 1222,
                PainIntensity.ANNOYING: 17333,
            },
        },
    },
    AnimalType.BROILER_CHICKEN: {
        BroilerChickenBreedingType.FREE_RANGE: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 70,
                PainIntensity.DISABLING: 2500,
                PainIntensity.HURTFUL: 4000,
                PainIntensity.ANNOYING: 18000,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 50,
                PainIntensity.DISABLING: 2000,
                PainIntensity.HURTFUL: 4000,
                PainIntensity.ANNOYING: 17000,
            },
        },
    },
    # Here will come data for other animals...
}


TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE = {
    AnimalType.LAYING_HEN: {
        LayingHenBreedingType.FREE_RANGE: ["en:free-range-chicken-eggs"],
        LayingHenBreedingType.BARN: ["en:barn-chicken-eggs"],
        LayingHenBreedingType.CAGE: ["en:cage-chicken-eggs"],
    },
    AnimalType.BROILER_CHICKEN: {
        # Can be tested with this barcode: 3256229237063
        # If you want to test with 2 animal products in the same product,
        # you can add the "en:poultry-hams" tag for on LAYING_HEN category
        # BroilerChickenBreedingType.FREE_RANGE: ["en:cooked-chicken-breast-slices"]
    },
}

COUNTRIES_WHERE_CAGES_ARE_FURNISHED = [
    "en:switzerland",  # conventional cages banned since 1992, phasing out of furnished cages
    "en:luxembourg",  # no more conventional cages since 2007, furnished cages to be phased out by 2025
    "en:sweden",  # cage systems banned
    "en:united-kingdom",  # conventional cages banned since 2012, transition to non-cage systems
    "en:france",  # EU regulations, ban on new conventional cage installations (2022)
    "en:germany",  # full exit from conventional cages by 2025, transition to furnished or cage-free systems
    "en:austria",  # total cage ban by 2025
    "en:netherlands",  # EU regulations
    "en:new-zealand",  # total cage ban in 2023
    "en:belgium",  # EU regulations
    "en:denmark",  # EU regulations
    "en:finland",  # EU regulations
    "en:ireland",  # EU regulations
    "en:italy",  # EU regulations
    "en:portugal",  # EU regulations
    "en:spain",  # EU regulations
    "en:poland",  # EU regulations
    "en:czech-republic",  # EU regulations
    "en:slovenia",  # EU regulations
    "en:croatia",  # EU regulations
    "en:bulgaria",  # EU regulations
    "en:hungary",  # EU regulations
    "en:latvia",  # EU regulations
    "en:lithuania",  # EU regulations
    "en:romania",  # EU regulations
    "en:estonia",  # EU regulations
    "en:greece",  # EU regulations
    "en:reunion",  # same as France
    "en:guadeloupe",  # same as France
    "en:martinique",  # same as France
    "en:mayotte",  # same as France
    "en:french-guiana",  # same as France
    "en:new-caledonia",  # same as France
]
