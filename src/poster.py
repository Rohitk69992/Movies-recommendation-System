"""
CineMatch — TMDB Poster Service Module
Safely retrieves and caches movie poster images with offline persistence,
campusx reference fallback credentials, and graceful typographic fallbacks.
"""

import json
import os
import urllib.parse
from typing import Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# In-memory cache for movie_id -> poster_url
_POSTER_CACHE: Dict[int, Optional[str]] = {}

# Local poster cache directory on disk
POSTER_CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "posters")
os.makedirs(POSTER_CACHE_DIR, exist_ok=True)

TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_API_URL = "https://api.themoviedb.org/3/movie/{movie_id}"
REQUEST_TIMEOUT_SECONDS = 4.0


def get_active_tmdb_api_key() -> str:
    """Return configured user TMDB API key from environment variable."""
    return os.getenv("TMDB_API_KEY", "").strip()


def generate_fallback_svg_raw(
    title: str = "Feature Film",
    year: Optional[int] = None,
    genre: Optional[str] = None
) -> str:
    """
    Generate valid XML SVG string for editorial archival film cover.
    Uses pure XML entities and valid escaping (never HTML entities like &bull;).
    """
    clean_title = (title[:30] + "...") if len(title) > 30 else title
    escaped_title = clean_title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;").replace('"', "&quot;")
    
    year_str = str(year) if year and year > 0 else "ARCHIVE"
    genre_str = (genre.upper() if genre else "CINEMA").replace("&", "&amp;")

    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='500' height='750' viewBox='0 0 500 750'>"
        f"<defs>"
        f"<linearGradient id='bgGrad' x1='0%' y1='0%' x2='100%' y2='100%'>"
        f"<stop offset='0%' stop-color='#14161d'/>"
        f"<stop offset='100%' stop-color='#0c0d12'/>"
        f"</linearGradient>"
        f"</defs>"
        f"<rect width='500' height='750' fill='url(#bgGrad)'/>"
        f"<rect x='24' y='24' width='452' height='702' fill='none' stroke='#262a36' stroke-width='1.5'/>"
        f"<rect x='32' y='32' width='436' height='686' fill='none' stroke='#1e212b' stroke-width='1'/>"
        f"<text x='250' y='72' fill='#c99a5b' font-family='Georgia, serif' font-size='13' font-weight='600' letter-spacing='5' text-anchor='middle'>CINEMATCH ARCHIVE</text>"
        f"<line x1='180' y1='88' x2='320' y2='88' stroke='#c99a5b' stroke-width='0.75' stroke-opacity='0.5'/>"
        f"<text x='250' y='360' fill='#f4f1ea' font-family='Georgia, serif' font-size='26' font-weight='500' text-anchor='middle'>{escaped_title}</text>"
        f"<line x1='200' y1='620' x2='300' y2='620' stroke='#3a3f50' stroke-width='1'/>"
        f"<text x='250' y='650' fill='#9ba1a6' font-family='sans-serif' font-size='13' font-weight='500' letter-spacing='3' text-anchor='middle'>{year_str} &#8226; {genre_str}</text>"
        f"</svg>"
    )


def generate_fallback_svg(
    title: str = "Feature Film",
    year: Optional[int] = None,
    genre: Optional[str] = None
) -> str:
    """Generate SVG as a data URI."""
    raw_svg = generate_fallback_svg_raw(title=title, year=year, genre=genre)
    escaped_svg = urllib.parse.quote(raw_svg)
    return f"data:image/svg+xml;utf8,{escaped_svg}"


def fetch_and_cache_poster(movie_id: int) -> Optional[str]:
    """
    Ensure the poster image for movie_id is downloaded and cached in data/posters/{movie_id}.jpg.
    Returns the absolute path to the local JPEG file, or None if unavailable.
    """
    target_path = os.path.join(POSTER_CACHE_DIR, f"{movie_id}.jpg")
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        return target_path

    api_key = get_active_tmdb_api_key()
    endpoint = TMDB_API_URL.format(movie_id=movie_id)
    params = {
        "api_key": api_key,
        "language": "en-US",
    }
    
    try:
        resp = requests.get(endpoint, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
        if resp.status_code == 200:
            data = resp.json()
            poster_path = data.get("poster_path")
            if poster_path:
                img_url = f"{TMDB_IMAGE_BASE}{poster_path}"
                img_resp = requests.get(img_url, timeout=5.0)
                if img_resp.status_code == 200 and len(img_resp.content) > 1000:
                    os.makedirs(POSTER_CACHE_DIR, exist_ok=True)
                    with open(target_path, "wb") as f:
                        f.write(img_resp.content)
                    return target_path
    except Exception:
        pass

    return None


def get_poster_url(
    movie_id: int,
    title: str = "Feature Film",
    year: Optional[int] = None,
    genre: Optional[str] = None
) -> str:
    """
    Retrieve poster image URL for a given TMDB movie ID.
    Points to the fast, reliable, local proxy endpoint /api/poster/{movie_id}.
    """
    return f"/api/poster/{movie_id}"


def get_tmdb_attribution_text() -> str:
    """Returns official TMDB attribution statement required under TMDB API Terms of Use."""
    return "This product uses the TMDB API but is not endorsed or certified by TMDB."
