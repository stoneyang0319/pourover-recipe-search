# app.py
import os
import sys
import textwrap
import streamlit as st
from exa_py import Exa

# ---- API key handling ----
API_KEY = os.environ.get("EXA_API_KEY") or st.secrets.get("EXA_API_KEY")
if not API_KEY:
    st.error(
        "EXA_API_KEY not found. Set it with:\n"
        "• export EXA_API_KEY='YOUR_KEY'\n"
        "or add to .streamlit/secrets.toml:\n"
        "[[secrets]]\nEXA_API_KEY='YOUR_KEY'\n"
    )
    st.stop()

exa = Exa(API_KEY)

# ---- Search function ----
@st.cache_data(show_spinner=False)
def search_coffee_recipes(varietal: str, brewing_method: str, num_results: int = 5):
    """
    Search for championship coffee recipes based on bean varietal and brewing method.
    Returns a list of Exa Result objects (with .title, .url, .text).
    """
    query = f"barista championship recipe {varietal} {brewing_method}"
    resp = exa.search_and_contents(
        query=query,
        num_results=num_results,
        type="auto",
        text={"max_characters": 5000},
        include_text=[varietal] if varietal else None,
    )
    # Note: resp.results is a list of Result objects
    return resp.results

# ---- UI ----
st.title("🏆 Championship Coffee Recipe Finder")

col1, col2 = st.columns(2)
with col1:
    bean = st.text_input("Bean Varietal", placeholder="Gesha, Bourbon, Ethiopia Yirgacheffe")
with col2:
    device = st.text_input("Brewing Device", placeholder="V60, AeroPress, Chemex")

num_results = st.slider("Number of results", 1, 10, 5)
run = st.button("Search Recipes", type="primary")

if run:
    if not bean and not device:
        st.warning("Enter at least a bean varietal or a brewing device.")
        st.stop()

    with st.spinner("Searching championship recipes…"):
        try:
            results = search_coffee_recipes(bean.strip(), device.strip(), num_results)
        except Exception as e:
            st.error(f"Search failed: {e}")
            st.stop()

    if not results:
        st.info("No results found. Try different keywords or increase result count.")
    else:
        for i, r in enumerate(results, start=1):
            with st.container(border=True):
                st.subheader(f"Recipe {i}: {getattr(r, 'title', 'Untitled')}")
                url = getattr(r, "url", None)
                if url:
                    st.write(f"Source: {url}")
                txt = getattr(r, "text", "") or ""
                # Keep it readable in the UI
                st.text_area(
                    f"Details (Result {i})",
                    textwrap.shorten(txt, width=4000, placeholder=" …"),
                    height=220,
                )
