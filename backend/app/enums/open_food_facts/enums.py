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
            "cage": _("Caged hen"),
            "conventional_cage": _("Battery hen"),
            "furnished_cage": _("Caged hen"),
            "barn": _("Barn hen"),
            "free_range": _("Free-range hen"),
        }
        return mappings.get(self.value, self.value)

    def icon_url(self) -> Optional[str]:
        return {
            "cage": "cage_icon.svg",
            "conventional_cage": "conventional_cage_icon.svg",
            "furnished_cage": "cage_icon.svg",
            "barn": "barn_icon.svg",
            "free_range": "free_range_icon.svg",
        }.get(self.value)

    def color(self) -> Optional[str]:
        return {
            "cage": "#be2F21",
            "conventional_cage": "#730a00",
            "furnished_cage": "#be2F21",
            "barn": "#ef7D19",
            "free_range": "#333333",
        }.get(self.value)

    def code(self) -> Optional[str]:
        return {
            "cage": "3",
            "conventional_cage": "3",
            "furnished_cage": "3",
            "barn": "2",
            "free_range": "0/1",
        }.get(self.value)


class BroilerChickenBreedingType(StrEnum):
    FREE_RANGE = auto()

    def translated_name(self, _: Callable) -> str:
        """Return the human-readable name for this breeding type"""
        mappings = {
            "free_range": _("Free range"),
        }
        return mappings.get(self.value, self.value)


BreedingType: TypeAlias = LayingHenBreedingType


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
        mappings = {"small": _("small"), "medium": _("medium"), "large": _("large"), "extra_large": _("extra large")}
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
        """Return the human-readable egg quantity."""

        if self.caliber:
            return text_manager.get_plural_text(
                quantity_texts.EGGS_WITH_CALIBER_SINGULAR,
                quantity_texts.EGGS_WITH_CALIBER_PLURAL,
                self.count,
            ).format(
                count=self.count,
                caliber=self.caliber.translated_name(_),
            )
        return text_manager.get_plural_text(
            quantity_texts.EGG_SINGULAR,
            quantity_texts.EGG_PLURAL,
            self.count,
        ).format(self.count)


ProductQuantity: TypeAlias = EggQuantity
