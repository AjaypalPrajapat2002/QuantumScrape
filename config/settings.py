"""Configuration and constants for QuantumScrape"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

FETCH_TIMEOUT = 15
MAX_LINKS_DISPLAY = 60
MAX_IMAGES_DISPLAY = 20
WORD_FREQUENCY_TOP_N = 20

STOP_WORDS = {
    "this", "that", "with", "from", "have", "been", "will", "they", "their",
    "what", "when", "which", "there", "were", "more", "also", "into", "than",
    "some", "your", "about", "would", "could", "should", "these", "those", "then"
}
