"""
Tests for TMDB Poster Module.
"""

import os
from src.poster import (
    get_poster_url, 
    generate_fallback_svg, 
    generate_fallback_svg_raw,
    get_tmdb_attribution_text,
    fetch_and_cache_poster
)


def test_fallback_svg_generation():
    svg_uri = generate_fallback_svg("Test Movie", year=2024, genre="Drama")
    assert svg_uri.startswith("data:image/svg+xml;utf8,")
    assert "CINEMATCH" in svg_uri


def test_fallback_svg_raw():
    svg_raw = generate_fallback_svg_raw("Test Movie", year=2024, genre="Drama")
    assert svg_raw.startswith("<svg")
    assert "CINEMATCH ARCHIVE" in svg_raw
    assert "Test Movie" in svg_raw


def test_get_poster_url_proxy():
    # Poster URL points to local high-reliability proxy endpoint
    url = get_poster_url(155, title="The Dark Knight")
    assert url == "/api/poster/155"


def test_fetch_and_cache_poster():
    # The Dark Knight (ID 155) should be present in local cache
    cached_path = fetch_and_cache_poster(155)
    assert cached_path is not None
    assert os.path.exists(cached_path)
    assert os.path.getsize(cached_path) > 1000


def test_attribution_text():
    text = get_tmdb_attribution_text()
    assert "TMDB" in text
    assert "not endorsed" in text
