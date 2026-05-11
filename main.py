"""QuantumScrape:Intelligent Web Mining and AI Summarization Platform"""

import streamlit as st
from bs4 import BeautifulSoup

# Import configuration and utilities
from config.settings import MAX_LINKS_DISPLAY, MAX_IMAGES_DISPLAY
from utils.fetch import fetch_url
from utils.extraction import extract_metadata, extract_links, extract_images, extract_text, extract_headings
from utils.export import to_json, to_csv

# Import UI components
from ui.styles import CUSTOM_CSS
from ui.components import render_header, render_url_input, render_error, render_stats, render_welcome_message
from ui.tabs import render_scraper_tab, render_metadata_tab, render_images_tab, render_analysis_tab
from ui.ai_tab import render_ai_extractor_tab


# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantumScrape",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─── UI ──────────────────────────────────────────────────────────────────────
render_header()

url, extract_btn = render_url_input()

# ─── State ───────────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "fetch_error" not in st.session_state:
    st.session_state.fetch_error = None

if extract_btn and url.strip():
    with st.spinner("Extracting data..."):
        try:
            html, final_url = fetch_url(url.strip())
            soup = BeautifulSoup(html, "html.parser")
            st.session_state.result = {
                "url": final_url,
                "meta": extract_metadata(soup, final_url),
                "links": extract_links(soup, final_url),
                "images": extract_images(soup, final_url),
                "text": extract_text(soup),
                "headings": extract_headings(soup),
                "html": html,
            }
            st.session_state.fetch_error = None
        except Exception as e:
            st.session_state.fetch_error = str(e)
            st.session_state.result = None

if st.session_state.fetch_error:
    render_error(st.session_state.fetch_error)

# ─── Results ─────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Stats row
    render_stats(r)

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Scraper", "🏷 Metadata", "🖼 Images", "📊 Analysis", "🤖 AI Extractor"])

    with tab1:
        render_scraper_tab(r)

    with tab2:
        render_metadata_tab(r)

    with tab3:
        render_images_tab(r)

    with tab4:
        render_analysis_tab(r)

    with tab5:
        render_ai_extractor_tab(r)

elif not extract_btn:
    render_welcome_message()
