"""
CineMatch — Preprocessing Module
Extracts and cleans structured metadata from TMDB JSON strings.
"""

import ast
import json
from typing import Any, List, Optional
import pandas as pd


def safe_literal_eval(val: Any) -> Any:
    """Safely parse a Python literal or JSON string."""
    if not isinstance(val, str) or not val.strip():
        return []
    try:
        return ast.literal_eval(val)
    except Exception:
        try:
            return json.loads(val)
        except Exception:
            return []


def extract_names(raw_text: Any) -> List[str]:
    """
    Extract 'name' property from serialized list of dictionaries.
    Used for genres and keywords.
    """
    parsed = safe_literal_eval(raw_text)
    if not isinstance(parsed, list):
        return []
    return [
        str(item["name"]).strip()
        for item in parsed
        if isinstance(item, dict) and "name" in item and item["name"]
    ]


def extract_top_cast(raw_text: Any, top_k: int = 3) -> List[str]:
    """
    Extract top-K actor names from serialized cast list.
    Faithful to CampusX convert3() / cast[:3] logic.
    """
    parsed = safe_literal_eval(raw_text)
    if not isinstance(parsed, list):
        return []
    names = []
    for item in parsed[:top_k]:
        if isinstance(item, dict) and "name" in item and item["name"]:
            names.append(str(item["name"]).strip())
    return names


def extract_director(raw_text: Any) -> List[str]:
    """
    Extract director name(s) from serialized crew list.
    Faithful to CampusX fetch_director() logic (crew job == 'Director').
    """
    parsed = safe_literal_eval(raw_text)
    if not isinstance(parsed, list):
        return []
    directors = []
    for item in parsed:
        if isinstance(item, dict) and item.get("job") == "Director" and "name" in item:
            name = str(item["name"]).strip()
            if name and name not in directors:
                directors.append(name)
    return directors


def collapse_spaces(names: List[str]) -> List[str]:
    """
    Remove interior spaces from entities to create atomic tokens.
    Faithful to CampusX collapse() function.
    Example: 'Sam Worthington' -> 'SamWorthington'
    """
    return [name.replace(" ", "") for name in names if name]


def preprocess_tmdb_metadata(
    df: pd.DataFrame,
    drop_null_overview: bool = True,
    cast_top_k: int = 3,
) -> pd.DataFrame:
    """
    Execute end-to-end preprocessing pipeline on raw TMDB metadata.

    Args:
        df: Raw merged dataframe.
        drop_null_overview: If True, drops rows with missing overview (CampusX style).
        cast_top_k: Number of lead actors to extract (default 3).

    Returns:
        Cleaned dataframe with parsed metadata columns.
    """
    cleaned = df.copy()

    # Handle missing overviews
    if drop_null_overview:
        cleaned = cleaned.dropna(subset=["overview"]).reset_index(drop=True)
    else:
        cleaned["overview"] = cleaned["overview"].fillna("")

    # Preserve human-readable display values
    cleaned["overview_display"] = cleaned["overview"].astype(str)
    
    # Extract structured fields
    cleaned["genres_clean"] = cleaned["genres"].apply(extract_names)
    cleaned["keywords_clean"] = cleaned["keywords"].apply(extract_names)
    cleaned["cast_clean"] = cleaned["cast"].apply(lambda x: extract_top_cast(x, top_k=cast_top_k))
    cleaned["crew_clean"] = cleaned["crew"].apply(extract_director)

    # Disambiguate with collapsed spaces for Bag-of-Words
    cleaned["genres_collapsed"] = cleaned["genres_clean"].apply(collapse_spaces)
    cleaned["keywords_collapsed"] = cleaned["keywords_clean"].apply(collapse_spaces)
    cleaned["cast_collapsed"] = cleaned["cast_clean"].apply(collapse_spaces)
    cleaned["crew_collapsed"] = cleaned["crew_clean"].apply(collapse_spaces)

    return cleaned
