"""
Tests for Feature Engineering Module.
"""

import pytest
import pandas as pd
from src.preprocessing import preprocess_tmdb_metadata
from src.feature_engineering import build_movie_tags, stem_text


def test_stem_text():
    assert stem_text("actions adventures dancing") == "action adventur danc"
    assert stem_text("") == ""


def test_build_movie_tags(sample_raw_movies_df, sample_raw_credits_df):
    merged = sample_raw_movies_df.merge(
        sample_raw_credits_df[["movie_id", "cast", "crew"]],
        left_on="id",
        right_on="movie_id"
    )
    cleaned = preprocess_tmdb_metadata(merged, drop_null_overview=True)
    featured = build_movie_tags(cleaned, apply_stemming=True)

    assert "tags" in featured.columns
    assert "release_year" in featured.columns

    # Check tags non-empty
    for tag in featured["tags"]:
        assert isinstance(tag, str)
        assert len(tag.strip()) > 0

    # Verify Space Odyssey has expected stemmed tokens
    tag0 = featured.iloc[0]["tags"]
    assert "stanleykubrick" in tag0
    assert "sciencefict" in tag0
    assert "space" in tag0
