from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional, TypeAlias


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
            "laying_hen": "en:eggs",
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

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable caliber"""
        mappings = {"small": _("Small"), "medium": _("Medium"), "large": _("Large"), "extra_large": _("Extra Large")}
        return mappings.get(self.value, self.value)


@dataclass
class EggQuantity:
    """
    Result of egg weight calculation containing all relevant information.

    Attributes:
        count: Number of eggs in the product
        caliber: Caliber of the eggs if known
        total_weight: Total weight of all eggs in grams
    """

    count: int
    total_weight: float
    caliber: EggCaliber | None = None

    @classmethod
    def from_count(cls, count: int, caliber: EggCaliber | None = None) -> Optional["EggQuantity"]:
        if count <= 0:
            return None
        egg_weight = caliber.weight if caliber else EggCaliber.AVERAGE.weight
        total_weight = count * egg_weight
        return cls(count=count, total_weight=total_weight, caliber=caliber)

    @classmethod
    def from_weight(cls, total_weight: float, caliber: EggCaliber | None = None) -> Optional["EggQuantity"]:
        if total_weight <= 0:
            return None
        egg_weight = caliber.weight if caliber else EggCaliber.AVERAGE.weight
        count = round(total_weight / egg_weight)
        return cls(count=count, total_weight=total_weight, caliber=caliber)

    def translated_display(self, _: Callable, text_manager, quantity_texts) -> str:
        """Return the human-readable egg quantity
        Args:
            text_manager: TextManager instance managing translations with plurals
            quantity_texts: QuantityTexts enum
            _: translation function

        Returns:
            str: Translated human-readable egg quantity eg. "12 Eggs - Large Caliber" or "12 Eggs"
        """
        quantity_text = text_manager.get_plural_text(
            quantity_texts.EGG_SINGULAR, quantity_texts.EGG_PLURAL, self.count
        ).format(self.count)
        if self.caliber:
            quantity_text += " - " + text_manager.get_text(quantity_texts.CALIBER).format(
                self.caliber.translated_name(_)
            )
        return quantity_text


ProductQuantity: TypeAlias = EggQuantity
