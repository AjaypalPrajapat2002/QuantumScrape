"""UI components for QuantumScrape"""

import streamlit as st
from urllib.parse import urlparse


def render_header():
    """Render the main header"""
    st.markdown('<div class="tagline">AI-Powered</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo">Quantum<span>Scrape</span> <span style="color:#333;font-size:1rem">· Python Edition</span></div>', unsafe_allow_html=True)
    st.markdown("---")


def render_url_input():
    """Render URL input field and extract button"""
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        url = st.text_input("", placeholder="https://example.com", label_visibility="collapsed")
    with col_btn:
        extract_btn = st.button("Extract", use_container_width=True)
    return url, extract_btn


def render_error(error_message):
    """Render error message"""
    st.markdown(f'<div class="error-box">⚠ {error_message}<br><br>'
                f'• Check the URL is correct and publicly accessible<br>'
                f'• Some sites block scrapers (Google, Instagram, Twitter)<br>'
                f'• Try: https://example.com or https://en.wikipedia.org/wiki/Python_(programming_language)</div>',
                unsafe_allow_html=True)


def render_stats(result):
    """Render statistics cards"""
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, num, label in [
        (c1, len(result["links"]), "Links"),
        (c2, len(result["images"]), "Images"),
        (c3, f"{len(result['text'])//1000}k", "Chars"),
        (c4, len(result["headings"]), "Headings"),
        (c5, len(result["meta"]), "Meta Tags"),
    ]:
        col.markdown(f'<div class="stat-card"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)


def render_welcome_message():
    """Render welcome message when no extraction done yet"""
    st.markdown("""
    <div style="text-align:center;padding:4rem 0;color:#222">
        <div style="font-family:'Space Mono',monospace;font-size:0.7rem;letter-spacing:3px;text-transform:uppercase;margin-bottom:1rem">Enter a URL above to begin</div>
        <div style="font-size:0.85rem;color:#1a1a2a;line-height:2.5">
            Scraper · Metadata · Images · Analysis · AI Extraction
        </div>
    </div>
    """, unsafe_allow_html=True)
