"""
Scrapes Tesco products for prices on specific products.
"""

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


try:
    soup = get_url_soup("milk")
    product_names = extract_product_names(soup)
    print(product_names)
except Exception as e:
    print(f"An error occurred: {e}")
