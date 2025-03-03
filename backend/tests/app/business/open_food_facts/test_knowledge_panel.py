from app.api.open_food_facts.schemas import PAIN_REPORT_EXAMPLE
from app.business.open_food_facts.knowledge_panel import get_properties_from_folksonomy


def test_get_properties_from_folksonomy():
    assert get_properties_from_folksonomy("1") == PAIN_REPORT_EXAMPLE


def test_get_properties_from_folksonomy_raises_an_error_and_logs_a_warning_if_the_product_is_not_found():
    # TODO
    pass
