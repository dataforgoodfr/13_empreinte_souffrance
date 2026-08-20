import io

from app.business.open_food_facts.calculators.unit_pain_loader import UnitPainLoader
from app.enums.open_food_facts.enums import AnimalType, EggCaliber, LayingHenBreedingType, PainIntensity, PainType


def test_load_minimal_csv():
    csv_content = """animal_type;breeding_type;pain_type;pain_intensity;caliber;pain_per_egg_in_seconds
laying_hen;barn;physical;hurtful;small;12.5
"""
    file_like = io.StringIO(csv_content)

    loader = UnitPainLoader(file_like)
    data = loader.load()

    assert isinstance(data, dict)
    assert AnimalType.LAYING_HEN in data
    assert LayingHenBreedingType.BARN in data[AnimalType.LAYING_HEN]
    assert PainType.PHYSICAL in data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN]
    assert PainIntensity.HURTFUL in data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN][PainType.PHYSICAL]
    assert (
        EggCaliber.SMALL
        in data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN][PainType.PHYSICAL][PainIntensity.HURTFUL]
    )
    assert (
        data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN][PainType.PHYSICAL][PainIntensity.HURTFUL][
            EggCaliber.SMALL
        ]
        == 12.5
    )
