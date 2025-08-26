from enum import Enum
from typing import Callable


class MainPanelTexts(Enum):
    """Texts for the main knowledge panel"""

    WELFARE_FOOTPRINT_INTRO = (
        "The <a href='https://empreinte-souffrance.org/'>Welfare Footprint</a> is calculated based "
        "on research from the <a href='https://welfarefootprint.org/'>Welfare Footprint Institute</a> "
        "which developed a scientifically rigorous methodology for assessing "
        "and quantifying animal welfare in food production systems."
    )

    WELFARE_FOOTPRINT_UNIQUENESS = (
        "It is unique in providing a comprehensive, biologically meaningful measure of "
        "the time animals spend in pain of varying intensities."
    )

    DATA_BASED_ON = (
        "The time in pain and details shown below are based on the following data "
        "(provided by the Open Food Facts community)"
    )

    MISSING_DATA = (
        "The time in pain could not be calculated for this product due to missing data "
        "in the Open Food Facts product description. You can contribute to the Open Food "
        "Facts community and help us calculate time in pain by filling in the missing information."
    )

    PANEL_TITLE = "Welfare footprint"
    PANEL_SUBTITLE = "What is the welfare footprint?"


class IntensityDefinitionTexts(Enum):
    """Texts for pain intensity definitions"""

    ANNOYING_DEFINITION = (
        "<b>Annoying</b>: Noticeable discomfort that can be ignored. Does not interfere with daily "
        "activities or motivated behaviors (exploration, comfort, maintenance). "
        "No visible expressions of pain or physiological disturbances."
    )

    HURTFUL_DEFINITION = (
        "<b>Hurtful</b>: Persistent pain with the possibility of brief moments of forgetting during "
        "distractions. Reduces the frequency of motivated behaviors and partially alters functional "
        "capabilities, while allowing essential activities to be carried out."
    )

    DISABLING_DEFINITION = (
        "<b>Disabling</b>: Constant pain that takes priority over most behaviors. "
        "Prevents positive well-being and drastically alters activity level. "
        "Requires stronger painkillers and causes inattention to the environment."
    )

    EXCRUCIATING_DEFINITION = (
        "<b>Excruciating</b>: Extreme unbearable pain, even briefly. "
        "In humans, this would mark the threshold of suffering below which many people "
        "choose to end their lives rather than endure it. Triggers involuntary manifestations "
        "(screams, tremors, extreme agitation) and cannot be relieved."
    )

    PANEL_TITLE = "Intensity categories definitions"


class PhysicalPainTexts(Enum):
    """Texts for physical pain panel"""

    DEFINITION = (
        "<b>Physical pain</b> includes all bodily suffering experienced by animals: "
        "fractures, wounds, diseases, breathing difficulties, etc."
    )

    DURATION_EXPLANATION = (
        "The durations below represent the suffering time caused "
        "by the production of animal-derived ingredients in this product:"
    )

    MORE_DETAILS = (
        "You can find more details about the different types of physical suffering "
        "<a href='https://empreinte-souffrance.org/'>on our website</a>."
    )

    PANEL_TITLE = "Physical pain"


class PsychologicalPainTexts(Enum):
    """Texts for psychological pain panel"""

    DEFINITION = (
        "<b>Psychological pain</b> includes mental suffering experienced by animals: "
        "stress, anxiety, inability to express natural behaviors, etc."
    )

    DURATION_EXPLANATION = (
        "The durations below represent the suffering time caused "
        "by the production of animal-derived ingredients in this product:"
    )

    MORE_DETAILS = (
        "You can find more details about the different types of psychological suffering "
        "<a href='https://empreinte-souffrance.org/'>on our website</a>."
    )

    PANEL_TITLE = "Psychological pain"


class AnimalInfoTexts(Enum):
    """Texts for animal information display"""

    ANIMAL_INFO_TEMPLATE = (
        "<b>{animal_name} :</b><ul>"
        "<li>Production system: <b>{breeding_type}</b></li>"
        "<li>Quantity in the product: <b>{quantity}</b></li></ul>"
    )

    NOT_FOUND = "Not found"


class DurationTexts(Enum):
    """Texts for duration formatting"""

    ZERO_SECOND = "0 second"
    DAY_SINGULAR = "{} day"
    DAY_PLURAL = "{} days"
    HOUR_SINGULAR = "{} hour"
    HOUR_PLURAL = "{} hours"
    MINUTE_SINGULAR = "{} minute"
    MINUTE_PLURAL = "{} minutes"
    SECOND_SINGULAR = "{} second"
    SECOND_PLURAL = "{} seconds"


class QuantityTexts(Enum):
    """Texts for quantity formatting"""

    EGG_SINGULAR = "{} Egg"
    EGG_PLURAL = "{} Eggs"
    CALIBER = "{} Caliber"


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
