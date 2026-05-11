"""URL fetching utilities"""

import requests
from config.settings import HEADERS, FETCH_TIMEOUT


def fetch_url(url):
    """Fetch HTML content from a URL"""
    if not url.startswith("http"):
        url = "https://" + url
    resp = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT, allow_redirects=True)
    resp.raise_for_status()
    return resp.text, url
