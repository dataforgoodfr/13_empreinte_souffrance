import pytest

from app.business.open_food_facts.panel_renderer.generator import EggKnowledgePanelGenerator
from app.config.i18n import I18N
from app.schemas.open_food_facts.internal import KnowledgePanelResponse, PainReport


# Test the display of knowledge panel with a product name or without it
@pytest.mark.parametrize(
    "product_name_for_test, expected_knowledge_panel_product_name",
    [
        ("Some product_name", "Some product_name"),
        (None, None),
    ],
)
# Test knowledge panel generation with a pain report with one animal and
# with a pain report with one animal with pain data and one animal without pain data
@pytest.mark.parametrize(
    "pain_report",
    ["pain_report", "pain_report_with_two_animals"],
    indirect=True,
)
def test_knowledge_panel_generator(
    pain_report: PainReport, product_name_for_test: str | None, expected_knowledge_panel_product_name: str | None
):
    """Test the EggKnowledgePanelGenerator with different pain_report fixtures and product names"""

    pain_report = pain_report.model_copy(update={"product_name": product_name_for_test})

    translator = I18N().get_translator(locale="en")

    # Create generator and test individual methods
    generator = EggKnowledgePanelGenerator(pain_reports=[pain_report], locale="en", translator=translator)

    # Test root panel
    root_panel = generator._create_root_panel(["project_panel"])

    assert root_panel.level == "info"
    assert root_panel.title_element.title == "Welfare footprint"
    assert len(root_panel.elements) >= 1
    assert any(
        el.text_element is not None and "physical pain" in el.text_element.html.lower()
        for el in root_panel.elements
        if el.element_type == "text"
    )
    # Test project panel
    intensities_panel = generator._create_project_panel()
    assert intensities_panel.title_element.title == "En savoir plus sur l'Empreinte Souffrance"
    assert len(intensities_panel.elements) >= 1

    # Test complete response
    response = generator.get_response()
    assert isinstance(response, KnowledgePanelResponse)
    assert len(response.panels) == 2

    # Verify that the product name in the response matches the expected value
    assert response.product.name == expected_knowledge_panel_product_name, (
        f"Product name in KnowledgePanelResponse should be \
            '{expected_knowledge_panel_product_name}' for input '{product_name_for_test}'"
    )


def test_knowledge_panel_generator_missing_quantity(pain_report_missing_quantity: PainReport):
    """Test the EggKnowledgePanelGenerator class with a pain report missing quantity"""
    translator = I18N().get_translator(locale="en")

    # Create generator and test individual methods
    generator = EggKnowledgePanelGenerator(
        pain_reports=[pain_report_missing_quantity], locale="en", translator=translator
    )

    # Test root panel
    root_panel = generator._create_root_panel([])
    assert root_panel.level == "info"
    assert root_panel.title_element.title == "Welfare footprint"

    # Test root panel elements as intro, uniqueness and missing data
    assert len(root_panel.elements) >= 1

    assert any(
        el.text_element is not None and "given for one egg" in el.text_element.html.lower()
        for el in root_panel.elements
        if el.element_type == "text"
    )

    # Test complete response
    response = generator.get_response()
    assert "root" in list(response.panels.keys())
    assert "project_panel" in list(response.panels.keys())
