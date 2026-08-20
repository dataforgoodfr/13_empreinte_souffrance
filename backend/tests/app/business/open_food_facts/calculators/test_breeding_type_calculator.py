import re

import pytest

from app.business.open_food_facts.calculators.breeding_type_calculator import (
    BreedingTypeCalculator,
    get_barn_regex,
    get_cage_regex,
    get_free_range_regex,
)


@pytest.mark.parametrize(
    "tag,should_match",
    [
        ("œufs-plein-air-non-bios", True),
        ("en:free-range-chicken-eggs", True),
        ("chicken-eggs-not-free-range", False),
        ("Ariaperta uova fresche da galline allevate all'aperto", True),
    ],
)
def test_free_range_regex(tag, should_match):
    pattern = get_free_range_regex()
    assert bool(re.search(pattern, BreedingTypeCalculator._clean(tag))) == should_match


@pytest.mark.parametrize(
    "tag,should_match",
    [
        ("œufs élevés AU SOL*", True),
        ("barn-chicken-eggs-not-organic", True),
        ("produit bio", False),
        ("oeufs solidaires", False),
    ],
)
def test_barn_regex(tag, should_match):
    pattern = get_barn_regex()
    assert bool(re.search(pattern, BreedingTypeCalculator._clean(tag))) == should_match


@pytest.mark.parametrize(
    "tag,should_match",
    [
        ("eggs-from-caged-hens", True),
        ("Produit hors Cage", False),
        ("abcagedd", False),
        ("cage-free-chicken-eggs", False),
        ("ces oeufs ne proviennent pas de poules éléveées en CAGE", False),
    ],
)
def test_cage_regex(tag, should_match):
    pattern = get_cage_regex()
    assert bool(re.search(pattern, BreedingTypeCalculator._clean(tag))) == should_match
