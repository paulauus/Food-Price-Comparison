"""
Scrapes Tesco products for prices on specific products.
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


def extract_product_names(query_html) -> list:
    """Returns the names of the first 5 search results as a list."""
    product_elements = query_html.find_all(
        "span", class_="styled__Text-sc-1i711qa-1 bsLJsh ddsweb-link__text")
    product_names = [product.get_text(strip=True)
                     for product in product_elements[:5]]
    return product_names


def main():
    # Set up argument parser for CLI
    parser = argparse.ArgumentParser(
        description="Scrape Tesco for product prices.")
    parser.add_argument("product_name", type=str,
                        help="The name of the product to search for")

    # Parse arguments
    args = parser.parse_args()

    # Scrape and display product names
    try:
        soup = get_url_soup(args.product_name)
        product_names = extract_product_names(soup)
        for product in product_names:
            print(product)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
