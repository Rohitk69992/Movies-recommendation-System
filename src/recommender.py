"""
CineMatch — Recommender Engine Module
Computes cosine similarity on CountVectorizer feature matrices and generates top-K recommendations.
"""

import os
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, load_npz, save_npz
import joblib


def _ensure_list(val: Any) -> List[Any]:
    """Helper to convert None, list, ndarray, or scalar into a Python list."""
    if val is None:
        return []
    if isinstance(val, np.ndarray):
        return val.tolist()
    if isinstance(val, list):
        return val
    return [val]


class ContentBasedRecommender:
    """
    Content-Based Movie Recommender faithful to CampusX methodology.
    Uses CountVectorizer bag-of-words and Cosine Similarity over synthesized metadata tags.
    """

    def __init__(
        self,
        max_features: int = 5000,
        stop_words: str = "english",
    ):
        self.max_features = max_features
        self.stop_words = stop_words
        self.vectorizer: Optional[CountVectorizer] = None
        self.feature_matrix: Optional[csr_matrix] = None
        self.movies_df: Optional[pd.DataFrame] = None
        self._id_to_idx: Dict[int, int] = {}
        self._title_to_indices: Dict[str, List[int]] = {}

    def fit(self, movies_df: pd.DataFrame) -> "ContentBasedRecommender":
        """
        Fit vectorizer and build feature matrix from preprocessed movies DataFrame.

        Args:
            movies_df: DataFrame with 'movie_id', 'title', and 'tags' columns.

        Returns:
            self
        """
        if "tags" not in movies_df.columns:
            raise ValueError("Input DataFrame must contain a 'tags' column.")
        if "movie_id" not in movies_df.columns:
            raise ValueError("Input DataFrame must contain a 'movie_id' column.")

        self.movies_df = movies_df.reset_index(drop=True).copy()

        # Vectorize
        self.vectorizer = CountVectorizer(
            max_features=self.max_features,
            stop_words=self.stop_words,
        )
        self.feature_matrix = self.vectorizer.fit_transform(self.movies_df["tags"])

        self._build_indices()
        return self

    def _build_indices(self) -> None:
        """Construct fast lookup maps for movie_id and title."""
        self._id_to_idx = {}
        self._title_to_indices = {}

        for idx, row in self.movies_df.iterrows():
            m_id = int(row["movie_id"])
            title = str(row["title"]).strip()
            self._id_to_idx[m_id] = idx

            title_lower = title.lower()
            if title_lower not in self._title_to_indices:
                self._title_to_indices[title_lower] = []
            self._title_to_indices[title_lower].append(idx)

    def get_movie_index(self, identifier: Union[int, str]) -> int:
        """
        Resolve a movie index from either an integer movie_id or title string.

        Args:
            identifier: movie_id (int) or title (str).

        Returns:
            Zero-based integer row index in movies_df.

        Raises:
            KeyError: If identifier cannot be resolved.
        """
        if self.movies_df is None:
            raise RuntimeError("Recommender model has not been fitted or loaded.")

        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            m_id = int(identifier)
            if m_id in self._id_to_idx:
                return self._id_to_idx[m_id]
            raise KeyError(f"Movie ID {m_id} not found in catalog.")

        title_str = str(identifier).strip().lower()
        if title_str in self._title_to_indices:
            return self._title_to_indices[title_str][0]

        # Fuzzy / substring search fallback
        matches = [t for t in self._title_to_indices if title_str in t]
        if matches:
            return self._title_to_indices[matches[0]][0]

        raise KeyError(f"Movie title '{identifier}' not found in catalog.")

    def compute_similarity_vector(self, query_idx: int) -> np.ndarray:
        """
        Compute cosine similarity of query movie against all movies in catalog.
        Uses sparse matrix dot product:
        cos(u, v) = (u . v) / (||u|| * ||v||)
        """
        if self.feature_matrix is None:
            raise RuntimeError("Feature matrix is not initialized.")

        query_vec = self.feature_matrix[query_idx]
        scores = cosine_similarity(query_vec, self.feature_matrix).flatten()
        return scores

    def recommend(
        self,
        identifier: Union[int, str],
        top_k: int = 5,
        exclude_self: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Generate top-K movie recommendations for a query movie.

        Args:
            identifier: movie_id (int) or title (str).
            top_k: Number of recommendations to return (default 5).
            exclude_self: Whether to exclude the query movie itself (default True).

        Returns:
            List of dictionaries containing recommended movie details and similarity scores.
        """
        if self.movies_df is None:
            raise RuntimeError("Recommender has not been fitted.")

        query_idx = self.get_movie_index(identifier)
        scores = self.compute_similarity_vector(query_idx).copy()

        if exclude_self:
            scores[query_idx] = -1.0

        # Vectorized sorting using numpy for ultra-low latency (< 1ms)
        # We fetch top candidates and sort deterministically
        k = min(max(1, top_k), len(scores) - (1 if exclude_self else 0))
        # Top k + 10 partition
        candidate_count = min(k + 20, len(scores))
        part_indices = np.argpartition(scores, -candidate_count)[-candidate_count:]
        
        # Sort candidates descending by score, tie-breaking by vote_average
        vote_averages = self.movies_df["vote_average"].fillna(0.0).values
        part_scores = scores[part_indices]
        part_votes = vote_averages[part_indices]

        # Lexicographical sort: -part_scores first, then -part_votes
        sorted_order = np.lexsort((-part_votes, -part_scores))
        selected_indices = part_indices[sorted_order][:k]

        query_tags_set = set(str(self.movies_df.iloc[query_idx]["tags"]).split())

        results = []
        for idx in selected_indices:
            score = float(scores[idx])
            if score < 0:
                continue

            row = self.movies_df.iloc[idx]
            cand_tags = set(str(row["tags"]).split())
            common_tokens = sorted(list(query_tags_set.intersection(cand_tags)))
            meaningful_common = [t for t in common_tokens if len(t) > 3][:6]

            genres = _ensure_list(row.get("genres_clean"))
            top_cast = _ensure_list(row.get("cast_clean"))
            crew = _ensure_list(row.get("crew_clean"))
            director = str(crew[0]) if crew else "Unknown"

            rec = {
                "movie_id": int(row["movie_id"]),
                "title": str(row["title"]),
                "release_year": int(row.get("release_year", 0)),
                "genres": genres,
                "director": director,
                "top_cast": top_cast,
                "overview": str(row.get("overview_display", row.get("overview", ""))),
                "vote_average": float(row.get("vote_average", 0.0)),
                "vote_count": int(row.get("vote_count", 0)),
                "similarity_score": round(score, 4),
                "similarity_percentage": round(score * 100, 1),
                "common_tags": meaningful_common,
            }
            results.append(rec)

        return results

    def save_artifacts(self, output_dir: str = "models") -> Dict[str, str]:
        """Save vectorizer, sparse matrix, and metadata table for fast deployment."""
        os.makedirs(output_dir, exist_ok=True)
        paths = {
            "metadata": os.path.join(output_dir, "movie_metadata.parquet"),
            "vectorizer": os.path.join(output_dir, "count_vectorizer.joblib"),
            "feature_matrix": os.path.join(output_dir, "feature_matrix.npz"),
        }

        keep_cols = [
            "movie_id", "title", "tags", "release_year", "overview_display",
            "genres_clean", "cast_clean", "crew_clean", "vote_average", "vote_count"
        ]
        available_cols = [c for c in keep_cols if c in self.movies_df.columns]
        self.movies_df[available_cols].to_parquet(paths["metadata"], index=False)

        joblib.dump(self.vectorizer, paths["vectorizer"])
        save_npz(paths["feature_matrix"], self.feature_matrix)

        return paths

    @classmethod
    def load_artifacts(cls, artifact_dir: str = "models") -> "ContentBasedRecommender":
        """Load saved artifacts and initialize the recommender engine."""
        meta_path = os.path.join(artifact_dir, "movie_metadata.parquet")
        vect_path = os.path.join(artifact_dir, "count_vectorizer.joblib")
        matrix_path = os.path.join(artifact_dir, "feature_matrix.npz")

        if not os.path.exists(meta_path) or not os.path.exists(matrix_path):
            raise FileNotFoundError(f"Missing required artifact files in {artifact_dir}")

        rec = cls()
        rec.movies_df = pd.read_parquet(meta_path)
        rec.vectorizer = joblib.load(vect_path) if os.path.exists(vect_path) else None
        rec.feature_matrix = load_npz(matrix_path)
        rec._build_indices()
        return rec
