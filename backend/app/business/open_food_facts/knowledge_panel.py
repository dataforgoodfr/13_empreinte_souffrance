import logging
from http.client import HTTPException

logger = logging.getLogger("app")


class ProductNotFoundException(Exception):
    pass


def get_properties_from_folksonomy(product_id) -> dict:
    """
    Retrieve product properties from Folksonomy Engine and return them, or None if
    :param product_id: The OFF product ID
    :return: The product properties or None if the product is not found in the Folksonomy Engine
    """

    try:
        # TODO: Retrieve knowledge panel data from Folksonomy Engine
        product_properties = {
            "score": 0.9,
        }
    except HTTPException as e:
        logger.warning(
            "Product not found", extra={"product_id": product_id, "error": str(e)},
        )
        raise ProductNotFoundException from e

    return product_properties
