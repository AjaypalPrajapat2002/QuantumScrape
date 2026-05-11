"""AI extraction tab component"""

import os
import streamlit as st
import requests
import json
from utils.export import to_json


def render_ai_extractor_tab(result):
    """Render AI Extractor tab content"""
    st.markdown("### AI Content Analyzer")
    st.caption("Uses Gemini AI to intelligently extract information from the page content.")

    prompt = st.text_area(
        "What do you want to extract?",
        value="Summarize this page and extract the key facts, main topics, and any important data points.",
        height=100
    )

    if st.button("🤖 Run AI Extraction"):
        with st.spinner("Gemini is analyzing..."):
            try:
                context = f"Page URL: {result['url']}\n\nPage Title: {result['meta'].get('Title','')}\n\nPage Text:\n{result['text'][:6000]}"
                gemini_api_key = os.getenv("GEMINI_API_KEY")
                if not gemini_api_key:
                    try:
                        gemini_api_key = st.secrets["GEMINI_API_KEY"]
                    except Exception:
                        gemini_api_key = None
                if not gemini_api_key:
                    raise ValueError("Gemini API key is missing. Set GEMINI_API_KEY in Streamlit secrets or the environment.")
                ai_resp = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
                    headers={"Content-Type": "application/json"},
                    params={"key": gemini_api_key},
                    json={
                        "contents": [{
                            "parts": [{
                                "text": f"You are an expert web content analyzer.\n\n{context}\n\n---\n\nUser request: {prompt}\n\nRespond clearly and concisely."
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 2048
                        }
                    },
                    timeout=30
                )
                if ai_resp.status_code != 200:
                    st.error(f"Gemini API error {ai_resp.status_code}: {ai_resp.text}")
                else:
                    data = ai_resp.json()
                    try:
                        result_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    except (KeyError, IndexError):
                        result_text = json.dumps(data, indent=2)
                    st.markdown("**AI Output:**")
                    st.markdown(f'<div class="section-card" style="line-height:1.8;font-size:0.9rem;color:#c8c8e0">{result_text}</div>', unsafe_allow_html=True)
                    st.download_button("⬇ Save AI Output", result_text, "ai_output.txt", "text/plain")
            except Exception as e:
                st.error(f"AI request failed: {e}")
