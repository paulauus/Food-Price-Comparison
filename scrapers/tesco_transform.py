"""
This is the transform script for scraping Tesco groceries from the shop's website.
"""

import re


def change_item_price_to_float(search_result: dict) -> float:
    """Changes all the item prices in the result into a float."""

    return float(search_result["item_price"].replace("£", ""))


def get_unit_price_float(search_result: dict) -> float:
    """Changes unit price into a float."""

    return float(search_result["unit_price"].split("/")[0].replace("£", ""))


def get_unit_name(search_result: dict) -> str:
    """Returns the unit name for unit price."""

    return search_result["unit_price"].split("/")[1]


def get_loyalty_item_price(search_result: dict) -> float:
    """Returns the loyalty price for the item as a float."""
    match = re.search(r'\b(?:£\d+\.\d{2}|\d+p)\b', search_result["loyalty_item_price"])

    if match:
        if "p" in match.group(0):
            return float(match.group(0).replace("p", ""))/ 100

        if "£" in match.group(0):
            return float(match.group(0).replace("£", ""))
    
    return change_item_price_to_float(search_result)


def get_loyalty_unit_price(search_result: dict) -> float:
    """Returns the unit price for loyalty prices as a float."""

    return float(search_result["loyalty_unit_price"].strip("()£").split("/")[0])


def main(extract_result: list[dict]) -> list[dict]:
    """Transforms the top 5 results into the correct data format to be used in data entry."""
    transformed_data = []

    for item in extract_result:
        transformed_item = {
            "product_name": item["product_name"],
            "item_price": change_item_price_to_float(item),
            "unit_price": get_unit_price_float(item),
            "unit_name": get_unit_name(item),
            "loyalty_item_price": get_loyalty_item_price(item),
            "loyalty_unit_price": get_loyalty_unit_price(item),
            "product_image_url": item["product_image_url"]
        }
        transformed_data.append(transformed_item)

    return transformed_data
