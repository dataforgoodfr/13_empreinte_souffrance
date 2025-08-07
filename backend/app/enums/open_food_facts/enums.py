from collections.abc import Callable
from enum import StrEnum, auto
from typing import TypeAlias


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


class BroilerChickenBreedingType(StrEnum):
    FREE_RANGE = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this breeding type"""
        mappings = {
            "free_range": _("Free range"),
        }
        return mappings.get(self.value, self.value)


BreedingType: TypeAlias = LayingHenBreedingType | BroilerChickenBreedingType


class AnimalType(StrEnum):
    LAYING_HEN = auto()
    BROILER_CHICKEN = auto()

    @property
    def categories_tags(self) -> str:
        return {
            "laying_hen": "en:chicken-eggs",
            "broiler_chicken": "en:chickens",
        }.get(self.value) or (_ for _ in ()).throw(ValueError(f"Unknown animal type: {self.value}"))

    @property
    def is_computed(self) -> bool:
        result = {
            "laying_hen": True,
            "broiler_chicken": False,
        }.get(self.value)
        if result is None:
            raise ValueError(f"Unknown animal type: {self.value}")
        return result

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this animal type"""
        mappings = {"laying_hen": _("Laying hen"), "broiler_chicken": _("Broiler chicken")}
        return mappings.get(self.value, self.value)


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


class EggCaliber(StrEnum):
    """Egg calibers with their corresponding weights in grams."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"

    AVERAGE = MEDIUM  # Default average caliber when not found

    @property
    def weight(self) -> int:
        return {
            EggCaliber.SMALL: 48,  # < 53g
            EggCaliber.MEDIUM: 58,  # 53g - 63g
            EggCaliber.LARGE: 68,  # 63g - 73g
            EggCaliber.EXTRA_LARGE: 78,  # > 73g
        }[self]
