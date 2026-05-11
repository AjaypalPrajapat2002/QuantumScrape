"""Content extraction utilities"""

from urllib.parse import urljoin, urlparse
import re
from collections import Counter
from config.settings import STOP_WORDS, WORD_FREQUENCY_TOP_N


def extract_metadata(soup, url):
    """Extract metadata from page"""
    def meta(name=None, prop=None):
        if name:
            tag = soup.find("meta", attrs={"name": name})
        elif prop:
            tag = soup.find("meta", attrs={"property": prop})
        else:
            return "—"
        return tag.get("content", "—") if tag else "—"

    return {
        "Title": soup.title.string.strip() if soup.title else meta(prop="og:title"),
        "Description": meta(name="description") or meta(prop="og:description"),
        "OG Title": meta(prop="og:title"),
        "OG Description": meta(prop="og:description"),
        "OG Image": meta(prop="og:image"),
        "OG Type": meta(prop="og:type"),
        "Keywords": meta(name="keywords"),
        "Author": meta(name="author"),
        "Robots": meta(name="robots"),
        "Viewport": meta(name="viewport"),
        "Theme Color": meta(name="theme-color"),
        "Charset": soup.meta.get("charset", "—") if soup.meta else "—",
        "Language": soup.html.get("lang", "—") if soup.html else "—",
        "Canonical": soup.find("link", rel="canonical")["href"] if soup.find("link", rel="canonical") else url,
    }


def extract_links(soup, base_url):
    """Extract all links from page"""
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full = urljoin(base_url, href)
        text = a.get_text(strip=True)[:80] or "(no text)"
        parsed = urlparse(full)
        if parsed.scheme in ("http", "https"):
            links.append({"url": full, "text": text, "domain": parsed.netloc})
    
    seen = set()
    unique = []
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"])
            unique.append(l)
    return unique


def extract_images(soup, base_url):
    """Extract all images from page"""
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src:
            continue
        full = urljoin(base_url, src)
        alt = img.get("alt", "")
        width = img.get("width", "")
        height = img.get("height", "")
        images.append({"url": full, "alt": alt, "width": width, "height": height})
    return images


def extract_text(soup):
    """Extract main text content from page"""
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines)


def extract_headings(soup):
    """Extract heading structure from page"""
    headings = []
    for tag in soup.find_all(["h1","h2","h3","h4","h5","h6"]):
        headings.append({"level": tag.name.upper(), "text": tag.get_text(strip=True)})
    return headings


def word_frequency(text, top_n=WORD_FREQUENCY_TOP_N):
    """Analyze word frequency in text"""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    words = [w for w in words if w not in STOP_WORDS]
    return Counter(words).most_common(top_n)
