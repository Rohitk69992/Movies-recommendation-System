"""
CineMatch — Feature Engineering Module
Transforms cleaned metadata into unified feature text tags for vectorization.
"""

from typing import List, Optional
import pandas as pd
from nltk.stem.porter import PorterStemmer


_stemmer = PorterStemmer()


def stem_text(text: str) -> str:
    """Apply Porter stemming to whitespace-delimited words."""
    if not text:
        return ""
    stemmed_words = [_stemmer.stem(word) for word in text.split()]
    return " ".join(stemmed_words)


def build_movie_tags(
    df: pd.DataFrame,
    apply_stemming: bool = True,
) -> pd.DataFrame:
    """
    Construct the final 'tags' text feature for each movie.
    Faithful to CampusX tag combination logic:
    tags = overview + genres + keywords + cast + crew

    Args:
        df: Preprocessed DataFrame containing *_collapsed and overview columns.
        apply_stemming: Whether to apply Porter stemming (recommended in CampusX lecture).

    Returns:
        DataFrame with added 'tags' and display metadata columns.
    """
    featured = df.copy()

    # 1. Overview tokenization (list of words)
    overview_tokens = featured["overview"].fillna("").apply(lambda x: str(x).lower().split())

    # 2. Combine all token lists
    tags_series = (
        overview_tokens
        + featured["genres_collapsed"].apply(lambda l: [x.lower() for x in l])
        + featured["keywords_collapsed"].apply(lambda l: [x.lower() for x in l])
        + featured["cast_collapsed"].apply(lambda l: [x.lower() for x in l])
        + featured["crew_collapsed"].apply(lambda l: [x.lower() for x in l])
    )

    # 3. Join tokens to single string
    joined_tags = tags_series.apply(lambda tokens: " ".join(tokens))

    # 4. Optional stemming
    if apply_stemming:
        joined_tags = joined_tags.apply(stem_text)

    featured["tags"] = joined_tags

    # Extract clean release year for UI display
    if "release_date" in featured.columns:
        featured["release_year"] = pd.to_datetime(
            featured["release_date"], errors="coerce"
        ).dt.year.fillna(0).astype(int)
    else:
        featured["release_year"] = 0

    return featured
