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


def extract_product_name(query_html: BeautifulSoup) -> list:
    """Returns the names of the first 5 search results as a list."""
    product_elements = query_html.find_all(
        "span", class_="styled__Text-sc-1i711qa-1 bsLJsh ddsweb-link__text")
    
    # Extract the name text from the first 5 results
    product_names = [product.get_text(strip=True)
                     for product in product_elements[:5]]
    
    return product_names


def extract_full_price(query_html: BeautifulSoup) -> list:
    """Returns the full price of the first 5 search results as a list."""
    # Change from 'span' to 'p' to match the correct HTML tag
    product_elements = query_html.find_all(
        "p", class_="text__StyledText-sc-1jpzi8m-0 gyHOWz ddsweb-text styled__PriceText-sc-v0qv7n-1 cXlRF")

    # Extract the price text from the first 5 results
    full_prices = [product.get_text(strip=True)
                   for product in product_elements[:5]]

    return full_prices


def extract_full_unit_price(query_html: BeautifulSoup) -> list:
    """Returns the full price of the first 5 search results as a list."""
    # Change from 'span' to 'p' to match the correct HTML tag
    product_elements = query_html.find_all(
        "p", class_="text__StyledText-sc-1jpzi8m-0 kiGrpI ddsweb-text styled__Subtext-sc-v0qv7n-2 kLkheV ddsweb-price__subtext")

    # Extract the price text from the first 5 results
    full_unit_prices = [product.get_text(strip=True)
                   for product in product_elements[:5]]

    return full_unit_prices


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
        product_names = extract_product_name(soup)
        for product in product_names:
            print(product)

        full_prices = extract_full_price(soup)
        for price in full_prices:
            print(price)

        full_unit_prices = extract_full_unit_price(soup)
        for price in full_unit_prices:
            print(price)

        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
