import requests

from app.api.open_food_facts.schemas import PAIN_REPORT_EXAMPLE, PainReport
from app.config.exceptions import ExternalServiceException, ResourceNotFoundException


def get_properties_from_folksonomy(barcode: str) -> PainReport:
    """
    Retrieve product properties from Folksonomy Engine.

    Args:
        barcode: The OpenFoodFacts product ID

    Returns:
        PainReport: The JSON stored in Folksonomy Engine for this product

    Raises:
        ResourceNotFoundException: If the product is not found
        ExternalServiceException: If there's an error accessing the folksonomy service
    """
    try:
        # TODO: Retrieve knowledge panel data from Folksonomy Engine
        # When implementing the actual API call, this would be something like:
        # response = requests.get(f"{FOLKSONOMY_API_URL}/products/{barcode}")
        # response.raise_for_status()  # Raises HTTPError for 4XX/5XX responses
        # product_properties = response.json()

        # For now, return mock data
        product_properties = PAIN_REPORT_EXAMPLE
    except requests.HTTPError as e:
        status_code = e.response.status_code

        if status_code == 404:
            raise ResourceNotFoundException(f"Product {barcode} not found") from e

        raise ExternalServiceException(f"Error accessing folksonomy service for product {barcode}, status code {status_code}") from e

    return product_properties
