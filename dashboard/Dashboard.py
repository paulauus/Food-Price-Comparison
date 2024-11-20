"""The main page of the interactive groceries dashboard."""

import sys
sys.path.append('../scrapers')

import streamlit as st

from tesco_extract import extract

search_query = st.text_input("Search for an item:", "")

result = extract(search_query)

for item in result:
    st.write(item)
