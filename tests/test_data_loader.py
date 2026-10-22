"""
Tests for Data Loader Module.
"""

import pytest
import pandas as pd
from src.data_loader import load_raw_tmdb_data


def test_load_raw_tmdb_data_success():
    """Verify loading real TMDB raw CSVs."""
    df = load_raw_tmdb_data(
        movies_path="data/raw/tmdb_5000_movies.csv",
        credits_path="data/raw/tmdb_5000_credits.csv",
        merge_on="id",
    )
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4803
    assert "movie_id" in df.columns
    assert "title" in df.columns
    assert "overview" in df.columns
    assert "genres" in df.columns
    assert "cast" in df.columns
    assert "crew" in df.columns


def test_load_raw_tmdb_data_missing_file():
    """Verify FileNotFoundError on nonexistent path."""
    with pytest.raises(FileNotFoundError):
        load_raw_tmdb_data(
            movies_path="nonexistent_movies.csv",
            credits_path="data/raw/tmdb_5000_credits.csv",
        )


def test_load_raw_tmdb_data_missing_column(tmp_path):
    """Verify ValueError when required column is missing."""
    bad_movies = tmp_path / "bad_movies.csv"
    bad_credits = tmp_path / "bad_credits.csv"

    pd.DataFrame({"id": [1], "name": ["A"]}).to_csv(bad_movies, index=False)
    pd.DataFrame({"movie_id": [1], "title": ["A"], "cast": ["[]"], "crew": ["[]"]}).to_csv(bad_credits, index=False)

    with pytest.raises(ValueError, match="Missing columns in movies file"):
        load_raw_tmdb_data(
            movies_path=str(bad_movies),
            credits_path=str(bad_credits),
        )
