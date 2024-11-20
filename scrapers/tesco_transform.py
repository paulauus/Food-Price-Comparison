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

if __name__ == "__main__":
    data = [{'product_name': 'Tesco Classic Round Tomatoes 6 Pack', 'item_price': '£0.95', 'unit_price': '£0.16/each', 'loyalty_item_price': '£0.95', 'loyalty_unit_price': '£0.16/each',
            'product_image_url': 'https://digitalcontent.api.tesco.com/v2/media/ghs/f8a5bbce-3cf5-4c3e-ba28-d1f7963c59b1/dcabae4b-8259-4f95-a3ec-33335f88fe0e.jpeg?h=225&w=225'}, {
                'product_name': 'Tesco Baby Plum Tomatoes 300G', 'item_price': '£1.00', 'unit_price': '£3.33/kg', 'loyalty_item_price': 'Save 25% 75p Clubcard Price', 'loyalty_unit_price': '(£2.50/kg)', 'product_image_url': 'https://digitalcontent.api.tesco.com/v2/media/ghs/479aeb6d-d911-44c3-8553-aade9b0d003c/8d0eeaf6-2c07-4766-8c5d-c3f8f84d6ca2.jpeg?h=225&w=225'}]
    print(change_item_price_to_float(data[1]))
    print(get_unit_price_float(data[1]))
    print(get_unit_name(data[1]))
    print(get_loyalty_item_price(data[1]))
