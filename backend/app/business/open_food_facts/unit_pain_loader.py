import csv
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, TextIO, TypeAlias

from app.enums.open_food_facts.enums import (
    AnimalType,
    BreedingType,
    EggCaliber,
    LayingHenBreedingType,
    PainIntensity,
    PainType,
)

LayingHenPainPerProductUnit: TypeAlias = Dict[
    AnimalType, Dict[BreedingType, Dict[PainType, Dict[PainIntensity, Dict[EggCaliber, float]]]]
]


class UnitPainLoader:
    """
    Loader for pain data per product from a CSV file.
    Specific to laying hens

    Attributes:
        csv_file: File-like object containing the CSV data.

    Columns expected in the CSV:
        - animal_type: Type of animal (e.g., "laying_hen")
        - breeding_type: Type of breeding (e.g., "furnished_cage")
        - pain_type: Type of pain (e.g., "physical")
        - pain_intensity: Intensity of pain (e.g., "excruciating")
        - caliber: Caliber of egg (e.g., "large")
        - pain_per_egg_in_seconds: Pain per egg in seconds (e.g., 30.0)
    """

    def __init__(self, csv_file: TextIO):
        self.csv_file = csv_file

    def load(self) -> LayingHenPainPerProductUnit:
        raw_data: DefaultDict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

        reader = csv.DictReader(self.csv_file, delimiter=";")
        for row in reader:
            try:
                animal = AnimalType(row["animal_type"])
                breeding = LayingHenBreedingType(row["breeding_type"])
                pain_type = PainType(row["pain_type"])
                intensity = PainIntensity(row["pain_intensity"])
                caliber = EggCaliber(row["caliber"])
                value = float(row["pain_per_egg_in_seconds"])

                raw_data[animal][breeding][pain_type][intensity][caliber] = value
            except (KeyError, ValueError) as e:
                raise ValueError(f"Ignored row in CSV pain data: {row} ({e})")

        return self._deep_convert(raw_data)

    def _deep_convert(self, d: dict | defaultdict) -> dict:
        if isinstance(d, defaultdict):
            return {k: self._deep_convert(v) for k, v in d.items()}
        return d


def get_pain_per_egg_data() -> LayingHenPainPerProductUnit:
    csv_path = Path(__file__).resolve().parent / "data" / "pain_data.csv"
    try:
        with csv_path.open(newline="", encoding="utf-8") as f:
            loader = UnitPainLoader(f)
            return loader.load()
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV pain data not found: {csv_path}")


PAIN_PER_EGG_IN_SECONDS = get_pain_per_egg_data()
