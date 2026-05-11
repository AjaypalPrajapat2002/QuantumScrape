# QuantumScrape — Complete Code Summary

> **Project:** QuantumScrape · Intelligent Web Mining and AI Summarization Platform  
> **Tech Stack:** Python, Streamlit, BeautifulSoup4, Requests, Gemini AI API

---

## Project Structure

```
WEB EXTRACTOR/
├── .streamlit/             # Streamlit configuration (empty)
├── config/
│   ├── __init__.py         # Makes config a Python package
│   └── settings.py         # Global constants & configuration
├── ui/
│   ├── __init__.py         # Makes ui a Python package
│   ├── ai_tab.py           # AI Extractor tab (Gemini integration)
│   ├── components.py       # Reusable UI widgets (header, stats, etc.)
│   ├── styles.py           # Custom CSS for the entire app
│   └── tabs.py             # Scraper, Metadata, Images & Analysis tabs
├── utils/
│   ├── __init__.py         # Makes utils a Python package
│   ├── export.py           # JSON & CSV export helpers
│   ├── extraction.py       # HTML parsing & data extraction logic
│   └── fetch.py            # HTTP request handler
└── main.py                 # Application entry point
```

---

## 1. `config/__init__.py` / `ui/__init__.py` / `utils/__init__.py`

These are **empty marker files**. They tell Python that `config/`, `ui/`, and `utils/` are **packages**, allowing `from config.settings import ...` style imports.

---

## 2. `config/settings.py` — Global Configuration

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `"""Configuration and constants..."""` | Module docstring describing the file's purpose. |
| 3-8 | `HEADERS = { "User-Agent": ..., "Accept": ..., "Accept-Language": ... }` | HTTP headers sent with every request. The User-Agent mimics Chrome so websites don't block the scraper. Accept tells servers we prefer HTML. Accept-Language requests English content. |
| 10 | `FETCH_TIMEOUT = 15` | Maximum seconds to wait for a server response before timing out. |
| 11 | `MAX_LINKS_DISPLAY = 60` | Cap for how many links are shown in the UI. |
| 12 | `MAX_IMAGES_DISPLAY = 20` | Cap for how many images are shown in the UI. |
| 13 | `WORD_FREQUENCY_TOP_N = 20` | Number of top words to display in frequency analysis. |
| 15-19 | `STOP_WORDS = {"this", "that", ...}` | A set of common English words to exclude from word-frequency analysis so results are meaningful. |

---

## 3. `utils/fetch.py` — URL Fetching

| Line | Code | Explanation |
|------|------|-------------|
| 1 | `"""URL fetching utilities"""` | Module docstring. |
| 3 | `import requests` | Imports the requests library for making HTTP calls. |
| 4 | `from config.settings import HEADERS, FETCH_TIMEOUT` | Imports browser-like headers and timeout value from settings. |
| 7 | `def fetch_url(url):` | Defines the function that downloads a webpage. |
| 8 | `"""Fetch HTML content from a URL"""` | Function docstring. |
| 9-10 | `if not url.startswith("http"): url = "https://" + url` | Auto-prepends `https://` if the user didn't type a protocol. |
| 11 | `resp = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT, allow_redirects=True)` | Sends an HTTP GET with fake browser headers, 15s timeout, follows redirects. |
| 12 | `resp.raise_for_status()` | Raises an exception if the HTTP status code indicates an error (4xx/5xx). |
| 13 | `return resp.text, url` | Returns the raw HTML string and the final URL. |

---

## 4. `utils/extraction.py` — Content Extraction

### `extract_metadata(soup, url)` — Lines 9-35

| Line | Code | Explanation |
|------|------|-------------|
| 9 | `def extract_metadata(soup, url):` | Takes a BeautifulSoup object and the page URL. |
| 11 | `def meta(name=None, prop=None):` | Inner helper to find `<meta>` tags by name or property attribute. |
| 12-13 | `if name: tag = soup.find("meta", attrs={"name": name})` | Searches for `<meta name="...">`. |
| 14-15 | `elif prop: tag = soup.find("meta", attrs={"property": prop})` | Searches for `<meta property="...">` (OpenGraph tags). |
| 16-17 | `else: return "—"` | Returns a dash if neither argument is given. |
| 18 | `return tag.get("content", "—") if tag else "—"` | Returns the content attribute, or dash if not found. |
| 20-35 | `return { "Title": ..., ... }` | Builds a dictionary with 14 metadata fields: Title, Description, OG tags, Keywords, Author, Robots, Viewport, Theme Color, Charset, Language, Canonical URL. |

### `extract_links(soup, base_url)` — Lines 38-55

| Line | Code | Explanation |
|------|------|-------------|
| 40 | `links = []` | Empty list to collect links. |
| 41 | `for a in soup.find_all("a", href=True):` | Iterates over every `<a>` tag with an href. |
| 42 | `href = a["href"].strip()` | Gets href value, removes whitespace. |
| 43 | `full = urljoin(base_url, href)` | Converts relative URLs to absolute URLs. |
| 44 | `text = a.get_text(strip=True)[:80] or "(no text)"` | Gets visible text (max 80 chars). |
| 45-47 | `parsed = urlparse(full) ...` | Parses URL, keeps only http/https, stores URL + text + domain. |
| 49-55 | `seen = set() ...` | Deduplicates links by URL, keeping first occurrence. |

### `extract_images(soup, base_url)` — Lines 58-70

| Line | Code | Explanation |
|------|------|-------------|
| 61 | `for img in soup.find_all("img"):` | Finds all `<img>` tags. |
| 62 | `src = img.get("src") or img.get("data-src") or ""` | Gets image source; tries data-src for lazy-loaded images. |
| 63-64 | `if not src: continue` | Skips images with no source. |
| 65 | `full = urljoin(base_url, src)` | Converts relative paths to absolute URLs. |
| 66-69 | `alt = img.get("alt", "") ...` | Extracts alt text, width, height, appends to list. |

### `extract_text(soup)` — Lines 73-79

| Line | Code | Explanation |
|------|------|-------------|
| 75-76 | `for tag in soup([...]): tag.decompose()` | Removes non-content elements (scripts, CSS, nav, footer, header, aside). |
| 77 | `text = soup.get_text(separator="\n")` | Extracts all visible text with newline separators. |
| 78 | `lines = [l.strip() for l in text.splitlines() if l.strip()]` | Strips whitespace, removes blank lines. |
| 79 | `return "\n".join(lines)` | Joins cleaned lines into a single string. |

### `extract_headings(soup)` — Lines 82-87

| Line | Code | Explanation |
|------|------|-------------|
| 85 | `for tag in soup.find_all(["h1",...,"h6"]):` | Finds all heading tags. |
| 86 | `headings.append({"level": ..., "text": ...})` | Stores each heading's level (H1-H6) and text content. |

### `word_frequency(text, top_n)` — Lines 90-94

| Line | Code | Explanation |
|------|------|-------------|
| 92 | `words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())` | Finds all words of 4+ letters. |
| 93 | `words = [w for w in words if w not in STOP_WORDS]` | Filters out stop words. |
| 94 | `return Counter(words).most_common(top_n)` | Returns top N most frequent words as (word, count) tuples. |

---

## 5. `utils/export.py` — Data Export

| Line | Code | Explanation |
|------|------|-------------|
| 3-5 | `import json, csv, io` | Imports JSON, CSV, and in-memory buffer modules. |
| 8-10 | `def to_json(data):` | Converts Python data to pretty-printed JSON string. `ensure_ascii=False` preserves Unicode. |
| 13-19 | `def to_csv(rows, fields):` | Converts list of dicts to CSV string. Uses `StringIO` as in-memory buffer. `extrasaction="ignore"` skips extra keys. |

---

## 6. `ui/styles.py` — Custom CSS

This file defines a single `CUSTOM_CSS` string containing a `<style>` block injected into the Streamlit app.

| Section | What It Styles |
|---------|---------------|
| Line 5 | Imports Google Fonts: `Space Mono` (monospace) and `Syne` (display headings). |
| Lines 7-16 | Dark background (`#0A0A0F`) and light text (`#E0E0F0`) for the entire app. |
| Lines 18-21 | Headings (h1-h3) with Syne font and neon green (`#00FFB2`). |
| Lines 23-41 | Logo and tagline with Space Mono font, custom sizing, letter-spacing. |
| Lines 43-64 | Stat cards: dark background (`#13131A`), borders, rounded corners, neon-green numbers. |
| Lines 66-81 | Section cards and card titles with consistent dark theme. |
| Lines 83-93 | Link items with monospace font, teal color, subtle green borders. |
| Lines 95-107 | Metadata keys (grey, uppercase) and values (light grey). |
| Lines 109-117 | Error box with red-tinted background and red text. |
| Lines 119-131 | Text input override to match dark theme, green glow on focus. |
| Lines 133-147 | Extract button: green background, black text, uppercase, hover opacity. |
| Lines 149-171 | Tab navigation: transparent background, green highlight for active tab. |
| Lines 173-184 | Text areas matching the dark theme. |
| Lines 186-195 | Download buttons: transparent with green outline. |
| Lines 197-202 | Select boxes matching the dark theme. |
| Lines 204-206 | Horizontal rules and spinner with green accent. |

---

## 7. `ui/components.py` — Reusable UI Widgets

| Function | Lines | What It Does |
|----------|-------|-------------|
| `render_header()` | 7-11 | Renders the app logo and tagline using raw HTML, followed by a horizontal divider. |
| `render_url_input()` | 14-21 | Creates a two-column layout: wide text input (5 parts) and narrow Extract button (1 part). Returns both values. |
| `render_error()` | 24-30 | Displays a styled error box with the error message and troubleshooting tips. |
| `render_stats()` | 33-43 | Creates a 5-column row of stat cards showing counts for Links, Images, Characters, Headings, Meta Tags. |
| `render_welcome_message()` | 46-55 | Shows a centered placeholder message when no URL has been extracted yet. |

---

## 8. `ui/tabs.py` — Tab Content Panels

### `render_scraper_tab(result)` — Lines 8-31

| Lines | What It Does |
|-------|-------------|
| 10-11 | Displays extracted text in a scrollable text area (300px). |
| 13-16 | Displays heading structure with visual indentation per level. |
| 18-22 | Lists up to 60 links with anchor text and URL. |
| 24-31 | Three download buttons: Links JSON, Links CSV, Text TXT. |

### `render_metadata_tab(result)` — Lines 34-48

| Lines | What It Does |
|-------|-------------|
| 36-40 | Displays metadata key-value pairs in a 2-column grid of styled cards. |
| 42-48 | Download buttons for metadata as JSON and CSV. |

### `render_images_tab(result)` — Lines 51-65

| Lines | What It Does |
|-------|-------------|
| 53-61 | Displays up to 20 images in a 4-column grid with captions. Falls back to text links on failure. |
| 63-65 | Download button for image data as JSON, or info message if no images found. |

### `render_analysis_tab(result)` — Lines 68-101

| Lines | What It Does |
|-------|-------------|
| 70-82 | Runs word frequency analysis; displays a bar chart and text-based frequency visualization. |
| 84-95 | Calculates page stats: word count, read time, internal vs external links using `st.metric()`. |
| 97-101 | Full JSON export button combining URL, metadata, stats, headings, and top words. |

---

## 9. `ui/ai_tab.py` — AI Extractor (Gemini Integration)

| Lines | What It Does |
|-------|-------------|
| 10-13 | Renders heading "AI Content Analyzer" with description caption. |
| 15-19 | Text area with default prompt asking for page summary. User can customize. |
| 21 | "Run AI Extraction" button triggers the API call. |
| 23-24 | Builds context string with page URL, title, and first 6000 chars of text. |
| 25-32 | Retrieves Gemini API key from environment variable or Streamlit secrets. Raises error if missing. |
| 33-48 | POST request to Gemini 2.5 Flash API with context + prompt, temperature 0.7, max 2048 tokens, 30s timeout. |
| 50-51 | Shows error if API returns non-200 status. |
| 52-57 | Parses response JSON to extract generated text. Falls back to raw JSON on parse failure. |
| 58-60 | Displays AI output in a styled card with download button. |
| 61-62 | Catches and displays any exceptions. |

---

## 10. `main.py` — Application Entry Point

| Lines | Code | Explanation |
|-------|------|-------------|
| 1 | `"""QuantumScrape:..."""` | Module docstring. |
| 3 | `import streamlit as st` | Imports Streamlit web framework. |
| 4 | `from bs4 import BeautifulSoup` | Imports the HTML parser. |
| 7 | `from config.settings import ...` | Imports display limit constants. |
| 8-10 | `from utils... import ...` | Imports fetch, extraction, and export functions. |
| 13-16 | `from ui... import ...` | Imports all UI components, tabs, styles, and AI tab. |
| 20-25 | `st.set_page_config(...)` | Configures page: title, icon, wide layout, sidebar collapsed. |
| 28 | `st.markdown(CUSTOM_CSS, ...)` | Injects custom CSS into the page. |
| 32 | `render_header()` | Draws the logo and tagline. |
| 34 | `url, extract_btn = render_url_input()` | Draws URL input and Extract button, captures values. |
| 37-40 | `if "result" not in st.session_state:` | Initializes session state for data persistence across reruns. |
| 42 | `if extract_btn and url.strip():` | Runs extraction only when button clicked AND URL provided. |
| 43 | `with st.spinner(...)` | Shows loading spinner during extraction. |
| 44-55 | `html, final_url = fetch_url(...)` | Fetches page, parses with BeautifulSoup, extracts all data into session state. |
| 56-59 | `except Exception as e:` | On failure, stores error and clears result. |
| 61-62 | `if st.session_state.fetch_error:` | Displays error box if an error exists. |
| 65-69 | `if st.session_state.result:` | If results exist, displays stat cards. |
| 71 | `st.markdown("---")` | Horizontal divider. |
| 74 | `st.tabs([...])` | Creates 5 tabs: Scraper, Metadata, Images, Analysis, AI Extractor. |
| 76-89 | `with tab1: ...` | Renders each tab's content. |
| 91-92 | `elif not extract_btn:` | Shows welcome message if nothing extracted yet. |

---

## Application Flow

```
User opens app
    └── main.py loads
        ├── Inject CSS + Render header
        ├── Show URL input + Extract button
        │
        ├── [No click] → Show welcome message
        │
        └── [Button clicked]
            ├── fetch_url() → Download HTML
            │   ├── [Error] → Show error box
            │   └── [Success] → BeautifulSoup parses HTML
            │       ├── extract_metadata()
            │       ├── extract_links()
            │       ├── extract_images()
            │       ├── extract_text()
            │       └── extract_headings()
            │
            └── Display results
                ├── Stat cards (links, images, chars, headings, meta)
                ├── Tab 1: Scraper (text + headings + links + downloads)
                ├── Tab 2: Metadata (key-value pairs + downloads)
                ├── Tab 3: Images (4-column grid + download)
                ├── Tab 4: Analysis (word freq + page stats + export)
                └── Tab 5: AI Extractor (Gemini prompt + output + download)
```

---

## Key Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web framework — handles UI, state, layout, and serving |
| **BeautifulSoup4** | HTML parsing and DOM traversal |
| **Requests** | HTTP client for fetching pages and calling Gemini API |
| **Google Gemini API** | AI-powered content summarization and extraction |
| **Python `re`** | Regex-based word extraction for frequency analysis |
| **Python `collections.Counter`** | Efficient word counting |
| **Python `csv` / `json`** | Data serialization for export downloads |
| **Python `urllib.parse`** | URL joining, parsing, and domain extraction |

---

## Summary

**QuantumScrape** is a modular Streamlit web application that scrapes any public webpage and presents the extracted data across 5 organized tabs. The architecture follows a clean separation of concerns:

- **`config/`** — Centralized settings (headers, limits, stop words)
- **`utils/`** — Pure logic (fetch, extract, export) — no UI code
- **`ui/`** — Pure presentation (styles, components, tabs) — no business logic
- **`main.py`** — Orchestrator that wires everything together

The app fetches HTML, parses it with BeautifulSoup, extracts structured data (metadata, links, images, text, headings), displays it in a polished dark-themed UI, offers JSON/CSV/TXT downloads, and optionally sends content to Google Gemini for AI-powered analysis.
