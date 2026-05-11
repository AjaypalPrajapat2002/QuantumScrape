"""Tab content components for QuantumScrape"""

import streamlit as st
from urllib.parse import urlparse
from utils.export import to_json, to_csv


def render_scraper_tab(result):
    """Render Scraper tab content"""
    st.markdown("### Extracted Text")
    st.text_area("", result["text"], height=300, label_visibility="collapsed")

    st.markdown("### Headings Structure")
    for h in result["headings"]:
        indent = {"H1":0,"H2":1,"H3":2,"H4":3,"H5":4,"H6":5}.get(h["level"],0)
        st.markdown(f'{"&nbsp;"*indent*4}<span style="color:#00FFB2;font-family:monospace;font-size:0.7rem">{h["level"]}</span> {h["text"]}', unsafe_allow_html=True)

    st.markdown("### Links")
    for l in result["links"][:60]:
        st.markdown(f'<div class="link-item"><b style="color:#fff">{l["text"]}</b><br>{l["url"]}</div>', unsafe_allow_html=True)
    if len(result["links"]) > 60:
        st.caption(f"...and {len(result['links'])-60} more links")

    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.download_button("⬇ Links JSON", to_json(result["links"]), "links.json", "application/json")
    with col_b:
        st.download_button("⬇ Links CSV", to_csv(result["links"], ["url","text","domain"]), "links.csv", "text/csv")
    with col_c:
        st.download_button("⬇ Text TXT", result["text"], "page_text.txt", "text/plain")


def render_metadata_tab(result):
    """Render Metadata tab content"""
    st.markdown("### Page Metadata")
    cols = st.columns(2)
    for i, (k, v) in enumerate(result["meta"].items()):
        with cols[i % 2]:
            st.markdown(f'<div class="section-card"><div class="meta-key">{k}</div><div class="meta-val">{v or "—"}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button("⬇ Metadata JSON", to_json(result["meta"]), "metadata.json", "application/json")
    with col_b:
        rows = [{"field": k, "value": v} for k, v in result["meta"].items()]
        st.download_button("⬇ Metadata CSV", to_csv(rows, ["field","value"]), "metadata.csv", "text/csv")


def render_images_tab(result):
    """Render Images tab content"""
    st.markdown(f"### Images Found ({len(result['images'])})")
    if result["images"]:
        grid = st.columns(4)
        for i, img in enumerate(result["images"][:20]):
            with grid[i % 4]:
                try:
                    st.image(img["url"], caption=img["alt"][:40] if img["alt"] else img["url"][-30:], use_container_width=True)
                except:
                    st.markdown(f'<div class="link-item">{img["url"]}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.download_button("⬇ Images JSON", to_json(result["images"]), "images.json", "application/json")
    else:
        st.info("No images found on this page.")


def render_analysis_tab(result):
    """Render Analysis tab content"""
    from utils.extraction import word_frequency
    
    st.markdown("### Word Frequency Analysis")
    freq = word_frequency(result["text"])
    if freq:
        words, counts = zip(*freq)
        import streamlit as _st
        chart_data = {"Word": list(words), "Count": list(counts)}
        st.bar_chart({"data": {w: c for w, c in freq}})
        st.markdown("**Top Words:**")
        for word, count in freq:
            bar = "█" * min(count, 40)
            st.markdown(f'<span style="font-family:monospace;font-size:0.8rem;color:#7af0cc">{word:<20}</span> <span style="color:#00FFB2">{bar}</span> <span style="color:#555">{count}</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Page Stats")
    words_total = len(result["text"].split())
    read_time = max(1, words_total // 200)
    internal = [l for l in result["links"] if urlparse(result["url"]).netloc in l["url"]]
    external = [l for l in result["links"] if urlparse(result["url"]).netloc not in l["url"]]

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Word Count", f"{words_total:,}")
    sc2.metric("Read Time", f"~{read_time} min")
    sc3.metric("Internal Links", len(internal))
    sc4.metric("External Links", len(external))

    st.download_button("⬇ Full JSON Export", to_json({
        "url": result["url"], "meta": result["meta"],
        "stats": {"words": words_total, "links": len(result["links"]), "images": len(result["images"])},
        "headings": result["headings"], "top_words": freq
    }), "full_report.json", "application/json")
