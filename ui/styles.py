"""Custom styling and CSS for QuantumScrape"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    background-color: #0A0A0F;
    color: #E0E0F0;
}

.main { background-color: #0A0A0F; }

.stApp {
    background: #0A0A0F;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #00FFB2 !important;
}

.logo {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #00FFB2;
    letter-spacing: -1px;
    margin-bottom: 0;
}

.logo span { color: #ffffff; }

.tagline {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #444;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

.stat-card {
    background: #13131A;
    border: 1px solid #1E1E2E;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}

.stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #00FFB2;
}

.stat-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #444;
}

.section-card {
    background: #13131A;
    border: 1px solid #1E1E2E;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

.card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #00FFB2;
    margin-bottom: 0.8rem;
}

.link-item {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #7af0cc;
    word-break: break-all;
    padding: 5px 10px;
    background: rgba(0,255,178,0.03);
    border-radius: 4px;
    border: 1px solid rgba(0,255,178,0.08);
    margin-bottom: 4px;
}

.meta-key {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.meta-val {
    font-size: 0.82rem;
    color: #ccc;
    word-break: break-all;
}

.error-box {
    background: rgba(255,60,60,0.06);
    border: 1px solid rgba(255,60,60,0.2);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #ff6060;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
}

div[data-testid="stTextInput"] input {
    background: #13131A !important;
    border: 1px solid #1E1E2E !important;
    border-radius: 8px !important;
    color: #E0E0F0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #00FFB2 !important;
    box-shadow: 0 0 0 1px #00FFB2 !important;
}

.stButton > button {
    background: #00FFB2 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover { opacity: 0.85 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1E1E2E !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #555 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1.4rem !important;
}

.stTabs [aria-selected="true"] {
    color: #00FFB2 !important;
    border-bottom: 2px solid #00FFB2 !important;
}

.stTextArea textarea {
    background: #13131A !important;
    border: 1px solid #1E1E2E !important;
    color: #E0E0F0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
}

.stTextArea textarea:focus {
    border-color: #00FFB2 !important;
}

div[data-testid="stDownloadButton"] button {
    background: transparent !important;
    color: #00FFB2 !important;
    border: 1px solid #00FFB2 !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
}

.stSelectbox > div > div {
    background: #13131A !important;
    border: 1px solid #1E1E2E !important;
    color: #E0E0F0 !important;
    border-radius: 8px !important;
}

hr { border-color: #1E1E2E !important; }

.stSpinner > div { border-top-color: #00FFB2 !important; }
</style>
"""
