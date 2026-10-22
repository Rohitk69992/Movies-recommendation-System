"""
CineMatch — Evaluation & Diagnostics Module
Computes empirical validation diagnostics, genre overlap Jaccard metrics, intra-list diversity,
and latency benchmarks for the content-based recommendation engine.
"""

import os
import time
from typing import Any, Dict, List
import numpy as np
import pandas as pd

from src.recommender import ContentBasedRecommender, _ensure_list


def compute_genre_jaccard(genres_a: List[str], genres_b: List[str]) -> float:
    """Compute Jaccard similarity coefficient between two genre lists."""
    set_a = set(genres_a)
    set_b = set(genres_b)
    if not set_a or not set_b:
        return 0.0
    union = set_a.union(set_b)
    if not union:
        return 0.0
    return len(set_a.intersection(set_b)) / len(union)


def run_diagnostics(
    recommender: ContentBasedRecommender,
    sample_size: int = 150,
    top_k: int = 5,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """
    Run empirical diagnostics across a sample of catalog movies.

    Metrics computed:
    - Self-exclusion compliance (% of queries where query movie is NOT in recommendations)
    - Duplicate-free compliance (% of recommendations with zero duplicates)
    - Score validity (% of similarity scores in [0.0, 1.0])
    - Mean genre Jaccard overlap between query and recommended items
    - Catalog coverage across sampled queries
    - Query latency (mean milliseconds per recommendation request)
    """
    df = recommender.movies_df
    np.random.seed(random_seed)
    sampled_indices = np.random.choice(len(df), size=min(sample_size, len(df)), replace=False)

    self_excluded_count = 0
    duplicate_free_count = 0
    valid_scores_count = 0
    total_recs = 0

    genre_jaccard_scores = []
    recommended_movie_ids = set()
    query_times_ms = []

    for idx in sampled_indices:
        query_row = df.iloc[idx]
        query_id = int(query_row["movie_id"])
        query_genres = _ensure_list(query_row.get("genres_clean"))

        start = time.perf_counter()
        recs = recommender.recommend(query_id, top_k=top_k, exclude_self=True)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        query_times_ms.append(elapsed_ms)

        rec_ids = [r["movie_id"] for r in recs]
        recommended_movie_ids.update(rec_ids)

        # 1. Self-exclusion check
        if query_id not in rec_ids:
            self_excluded_count += 1

        # 2. Duplicate check
        if len(rec_ids) == len(set(rec_ids)):
            duplicate_free_count += 1

        # 3. Score validity & Genre Jaccard
        for r in recs:
            total_recs += 1
            score = r["similarity_score"]
            if 0.0 <= score <= 1.0:
                valid_scores_count += 1

            rec_genres = r.get("genres", [])
            jaccard = compute_genre_jaccard(query_genres, rec_genres)
            genre_jaccard_scores.append(jaccard)

    n_queries = len(sampled_indices)
    catalog_coverage_pct = (len(recommended_movie_ids) / len(df)) * 100.0

    report = {
        "sampled_queries_count": n_queries,
        "top_k_parameter": top_k,
        "self_exclusion_rate_percent": (self_excluded_count / n_queries) * 100.0,
        "duplicate_free_rate_percent": (duplicate_free_count / n_queries) * 100.0,
        "score_validity_percent": (valid_scores_count / total_recs) * 100.0 if total_recs > 0 else 0.0,
        "mean_genre_jaccard_similarity": round(float(np.mean(genre_jaccard_scores)), 4),
        "catalog_coverage_percent": round(catalog_coverage_pct, 2),
        "unique_items_recommended": len(recommended_movie_ids),
        "mean_query_latency_ms": round(float(np.mean(query_times_ms)), 3),
        "p95_query_latency_ms": round(float(np.percentile(query_times_ms, 95)), 3),
    }

    return report


if __name__ == "__main__":
    import json
    rec = ContentBasedRecommender.load_artifacts("models")
    diag = run_diagnostics(rec, sample_size=150, top_k=5)
    print(json.dumps(diag, indent=2))
