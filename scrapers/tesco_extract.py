"""
This is the extract script for scraping Tesco groceries from the shop's website.
"""

import argparse

from bs4 import BeautifulSoup
from curl_cffi import requests


def get_url_soup(item: str) -> BeautifulSoup:
    """Returns a soup object from a URL for the given item, using curl_cffi for impersonation."""
    url = f"https://www.tesco.com/groceries/en-GB/search?query={
        item}&inputType=free+text"

    # Set up impersonation to mimic a browser request
    response = requests.get(
        url,
        # or try "chrome114", "firefox102" depending on the website’s response
        impersonate="chrome110"
    )

    # Parse response HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    return soup


def extract_html_under_div(query_html: BeautifulSoup) -> list[BeautifulSoup]:
    """Returns the HTML content under each <div class="_ecrj"> for the first 5 results."""
    # Find all divs with class '_ecrj' which represent product containers
    div_elements = query_html.find_all("div", class_="_ecrj")[:5]
    return div_elements


def extract_product_name(product_html: BeautifulSoup) -> str:
    """Extracts the product name from a single product's HTML."""
    name_element = product_html.find(
        "span", class_="styled__Text-sc-1i711qa-1 bsLJsh ddsweb-link__text")
    return name_element.get_text(strip=True) if name_element else "N/A"


def extract_full_price(product_html: BeautifulSoup) -> str:
    """Extracts the full price from a single product's HTML."""
    price_element = product_html.find(
        "p", class_="text__StyledText-sc-1jpzi8m-0 gyHOWz ddsweb-text styled__PriceText-sc-v0qv7n-1 cXlRF")
    return price_element.get_text(strip=True) if price_element else "N/A"


def extract_full_unit_price(product_html: BeautifulSoup) -> str:
    """Extracts the full unit price from a single product's HTML."""
    unit_price_element = product_html.find(
        "p", class_="text__StyledText-sc-1jpzi8m-0 kiGrpI ddsweb-text styled__Subtext-sc-v0qv7n-2 kLkheV ddsweb-price__subtext")
    return unit_price_element.get_text(strip=True) if unit_price_element else "N/A"


def extract_loyalty_full_price(product_html: BeautifulSoup) -> str:
    """Extracts the loyalty full price. If loyalty price exists, return it; otherwise, return the full price."""
    # Try to find the loyalty price element
    loyalty_price_element = product_html.find(
        "p", class_="text__StyledText-sc-1jpzi8m-0 gljcji ddsweb-text styled__ContentText-sc-1d7lp92-8 kjLZec ddsweb-value-bar__content-text")

    # If loyalty price exists, return it
    if loyalty_price_element:
        return loyalty_price_element.get_text(strip=True)

    # Otherwise, return the full price as the loyalty price
    return extract_full_price(product_html)


def extract_loyalty_unit_price(product_html: BeautifulSoup) -> str:
    """Extracts the loyalty unit price. If loyalty unit price exists, return it; otherwise, return the full unit price."""
    # Try to find the loyalty unit price element
    loyalty_unit_price_element = product_html.find(
        "p", class_="text__StyledText-sc-1jpzi8m-0 ggFawa ddsweb-text styled__SubText-sc-1d7lp92-10 jccqnm ddsweb-value-bar__content-subtext")

    # If loyalty unit price exists, return it
    if loyalty_unit_price_element:
        return loyalty_unit_price_element.get_text(strip=True)

    # Otherwise, return the full unit price as the loyalty unit price
    return extract_full_unit_price(product_html)


def extract_image_url(product_html: BeautifulSoup) -> str:
    """Extracts the image URL from a single product's HTML."""
    img_element = product_html.find(
        "img", class_="styled__StyledImage-sc-1fweb41-1 fMufzB")
    
    return img_element["src"] if img_element else None


def extract() -> list[dict]:
    """Extracts the top 5 search result items info from the groceries website."""
    # Set up argument parser for CLI
    parser = argparse.ArgumentParser(
        description="Scrape Tesco for product prices.")
    parser.add_argument("product_name", type=str,
                        help="The name of the product to search for")

    # Parse arguments
    args = parser.parse_args()

    # Scrape the soup for the given product
    try:
        soup = get_url_soup(args.product_name)

        # Extract HTML content for each product container
        product_containers = extract_html_under_div(soup)

        result = []
        # Loop through each product container and extract relevant data
        for product_html in product_containers:

            product = {}

            product["product_name"] = extract_product_name(product_html)
            product["item_price"] = extract_full_price(product_html)
            product["unit_price"] = extract_full_unit_price(product_html)
            product["loyalty_item_price"] = extract_loyalty_full_price(product_html)
            product["loyalty_unit_price"] = extract_loyalty_unit_price(product_html)
            product["product_image_url"] = extract_image_url(product_html)

            result.append(product)

    except Exception as e:
        print(f"An error occurred: {e}")

    return result


if __name__ == "__main__":
    result = extract()
    for item in result:
        print(item)
