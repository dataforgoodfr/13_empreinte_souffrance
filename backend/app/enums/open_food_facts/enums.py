import os
from collections.abc import Callable
from enum import StrEnum, auto
from typing import TypeAlias

import pandas as pd

base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "pain_data.csv")


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

PAIN_PER_EGG = pd.read_csv(csv_path, sep=";", decimal=",")


TIME_IN_PAIN_FOR_AN_EGG_IN_SECONDS = {
    AnimalType.LAYING_HEN: {
        LayingHenBreedingType.CONVENTIONAL_CAGE: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 0.5,
                PainIntensity.DISABLING: 1089.6,
                PainIntensity.HURTFUL: 12125.6,
                PainIntensity.ANNOYING: 11968.8,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 0,
                PainIntensity.DISABLING: 4087.4,
                PainIntensity.HURTFUL: 36504.4,
                PainIntensity.ANNOYING: 68040.0,
            },
        },
        LayingHenBreedingType.FURNISHED_CAGE: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 0.5,
                PainIntensity.DISABLING: 1165.9,
                PainIntensity.HURTFUL: 14660.4,
                PainIntensity.ANNOYING: 14587.7,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 0,
                PainIntensity.DISABLING: 688.1,
                PainIntensity.HURTFUL: 23156.3,
                PainIntensity.ANNOYING: 59115.0,
            },
        },
        LayingHenBreedingType.BARN: {
            PainType.PHYSICAL: {
                PainIntensity.EXCRUCIATING: 0.5,
                PainIntensity.DISABLING: 1475.9,
                PainIntensity.HURTFUL: 18805.0,
                PainIntensity.ANNOYING: 18353.6,
            },
            PainType.PSYCHOLOGICAL: {
                PainIntensity.EXCRUCIATING: 0,
                PainIntensity.DISABLING: 396.7,
                PainIntensity.HURTFUL: 2098.2,
                PainIntensity.ANNOYING: 3732.7,
            },
        },
        # To be deleted or replaced by the new data
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
}
