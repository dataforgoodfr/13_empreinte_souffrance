from enum import Enum
from typing import Callable


class RootPanelTexts(Enum):
    """Texts for the main knowledge panel"""

    PANEL_TITLE = "Welfare footprint"
    PANEL_SUBTITLE = "What is the welfare footprint?"


class DurationTexts(Enum):
    """Texts for duration formatting"""

    ZERO_SECOND = " -"
    DAY_SINGULAR = "{} day"
    DAY_PLURAL = "{} days"
    HOUR_SINGULAR = "{} hour"
    HOUR_PLURAL = "{} hours"
    MINUTE_SINGULAR = "{} minute"
    MINUTE_PLURAL = "{} minutes"
    SECOND_SINGULAR = "{} second"
    SECOND_PLURAL = "{} seconds"


class QuantityTexts(str, Enum):
    """Texts for quantity formatting"""

    EGG_SINGULAR = "{} egg contains on average"
    EGG_PLURAL = "{} eggs contain on average"
    EGGS_WITH_CALIBER_SINGULAR = "{count} {caliber} caliber egg contains on average"
    EGGS_WITH_CALIBER_PLURAL = "{count} {caliber} caliber eggs contain on average"


class PanelTextManager:
    """Helper class to manage panel texts with translation"""

    def __init__(self, translator: tuple[Callable, Callable]):
        self._ = translator[0]
        self._n = translator[1]

    def get_text(self, text_enum: Enum) -> str:
        """Get translated text from enum"""
        return self._(text_enum.value)

    def get_plural_text(self, text_enum_singular: Enum, text_enum_plural: Enum, count: int) -> str:
        """Get translated plural text"""
        return self._n(text_enum_singular.value, text_enum_plural.value, count)

    def format_text(self, text_enum: Enum, **kwargs) -> str:
        """Get translated text and format it with provided arguments"""
        return self._(text_enum.value).format(**kwargs)
