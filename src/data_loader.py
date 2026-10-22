"""
CineMatch — Data Loader Module
Loads raw TMDB 5000 movies and credits datasets safely.
"""

import os
from typing import Optional, Tuple
import pandas as pd


def load_raw_tmdb_data(
    movies_path: str = "data/raw/tmdb_5000_movies.csv",
    credits_path: str = "data/raw/tmdb_5000_credits.csv",
    merge_on: str = "id",
) -> pd.DataFrame:
    """
    Load raw TMDB movies and credits CSV files and merge them.

    Args:
        movies_path: Path to tmdb_5000_movies.csv.
        credits_path: Path to tmdb_5000_credits.csv.
        merge_on: Key to merge on: 'id' (modernized, safe) or 'title' (CampusX legacy).

    Returns:
        Merged pandas DataFrame with validated metadata.

    Raises:
        FileNotFoundError: If input files do not exist.
        ValueError: If required columns are missing.
    """
    if not os.path.exists(movies_path):
        raise FileNotFoundError(f"Movies CSV not found at: {movies_path}")
    if not os.path.exists(credits_path):
        raise FileNotFoundError(f"Credits CSV not found at: {credits_path}")

    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # Validate essential schema
    required_movies_cols = {"id", "title", "overview", "genres", "keywords"}
    required_credits_cols = {"movie_id", "title", "cast", "crew"}

    missing_m = required_movies_cols - set(movies.columns)
    if missing_m:
        raise ValueError(f"Missing columns in movies file: {missing_m}")

    missing_c = required_credits_cols - set(credits.columns)
    if missing_c:
        raise ValueError(f"Missing columns in credits file: {missing_c}")

    if merge_on == "title":
        # CampusX original notebook merge on 'title'
        merged = movies.merge(credits, on="title")
        if "movie_id" not in merged.columns and "id" in merged.columns:
            merged["movie_id"] = merged["id"]
    else:
        # Modernized safe merge on id == movie_id
        merged = movies.merge(
            credits[["movie_id", "cast", "crew"]],
            left_on="id",
            right_on="movie_id",
            how="inner",
        )

    # Standardize movie_id
    if "movie_id" not in merged.columns and "id" in merged.columns:
        merged["movie_id"] = merged["id"]

    return merged
