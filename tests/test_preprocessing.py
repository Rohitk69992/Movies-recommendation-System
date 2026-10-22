"""
Tests for Preprocessing Module.
"""

import pytest
import pandas as pd
from src.preprocessing import (
    extract_names,
    extract_top_cast,
    extract_director,
    collapse_spaces,
    preprocess_tmdb_metadata,
)


def test_extract_names_valid():
    raw = '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}]'
    assert extract_names(raw) == ["Action", "Adventure"]


def test_extract_names_empty_and_invalid():
    assert extract_names("[]") == []
    assert extract_names("") == []
    assert extract_names(None) == []
    assert extract_names("invalid json text") == []


def test_extract_top_cast():
    raw = '[{"name": "Actor 1"}, {"name": "Actor 2"}, {"name": "Actor 3"}, {"name": "Actor 4"}]'
    # Default top 3
    assert extract_top_cast(raw, top_k=3) == ["Actor 1", "Actor 2", "Actor 3"]
    # Custom top 2
    assert extract_top_cast(raw, top_k=2) == ["Actor 1", "Actor 2"]


def test_extract_director():
    raw = '[{"name": "James Cameron", "job": "Director"}, {"name": "Jon Landau", "job": "Producer"}]'
    assert extract_director(raw) == ["James Cameron"]

    raw_no_dir = '[{"name": "Jon Landau", "job": "Producer"}]'
    assert extract_director(raw_no_dir) == []


def test_collapse_spaces():
    names = ["Sam Worthington", "Science Fiction", "Christopher Nolan"]
    expected = ["SamWorthington", "ScienceFiction", "ChristopherNolan"]
    assert collapse_spaces(names) == expected
    assert collapse_spaces([]) == []


def test_preprocess_tmdb_metadata(sample_raw_movies_df, sample_raw_credits_df):
    merged = sample_raw_movies_df.merge(
        sample_raw_credits_df[["movie_id", "cast", "crew"]],
        left_on="id",
        right_on="movie_id"
    )
    # Total input: 4 rows, 1 has null overview
    cleaned = preprocess_tmdb_metadata(merged, drop_null_overview=True)
    assert len(cleaned) == 3
    assert "genres_collapsed" in cleaned.columns
    assert "cast_collapsed" in cleaned.columns
    assert "crew_collapsed" in cleaned.columns

    # First movie (Space Odyssey) checks
    row0 = cleaned.iloc[0]
    assert "ScienceFiction" in row0["genres_collapsed"]
    assert "StanleyKubrick" in row0["crew_collapsed"]
    assert "KeirDullea" in row0["cast_collapsed"]
