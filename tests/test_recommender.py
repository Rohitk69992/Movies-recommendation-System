"""
Tests for Recommender Engine Module.
"""

import os
import pytest
import pandas as pd
from src.preprocessing import preprocess_tmdb_metadata
from src.feature_engineering import build_movie_tags
from src.recommender import ContentBasedRecommender


@pytest.fixture
def fitted_toy_recommender(sample_raw_movies_df, sample_raw_credits_df):
    merged = sample_raw_movies_df.merge(
        sample_raw_credits_df[["movie_id", "cast", "crew"]],
        left_on="id",
        right_on="movie_id"
    )
    cleaned = preprocess_tmdb_metadata(merged, drop_null_overview=True)
    featured = build_movie_tags(cleaned, apply_stemming=True)
    rec = ContentBasedRecommender(max_features=100)
    rec.fit(featured)
    return rec


def test_recommender_get_index(fitted_toy_recommender):
    rec = fitted_toy_recommender
    # By ID
    assert rec.get_movie_index(101) == 0
    # By Title exact
    assert rec.get_movie_index("Space Odyssey") == 0
    # Case insensitive
    assert rec.get_movie_index("space odyssey") == 0
    # Substring / fuzzy
    assert rec.get_movie_index("odyssey") == 0

    # Nonexistent
    with pytest.raises(KeyError):
        rec.get_movie_index(99999)
    with pytest.raises(KeyError):
        rec.get_movie_index("Completely Nonexistent Title XYZ")


def test_recommender_recommendation_logic(fitted_toy_recommender):
    rec = fitted_toy_recommender
    # Recommend for Space Odyssey (id 101)
    recs = rec.recommend(101, top_k=2, exclude_self=True)

    assert len(recs) == 2
    # Check self-exclusion
    rec_ids = [r["movie_id"] for r in recs]
    assert 101 not in rec_ids

    # Solar Wind (id 102) shares Stanley Kubrick and sci-fi keywords with Space Odyssey,
    # so it should rank higher than romance film 'Love in Paris' (id 103)
    assert recs[0]["movie_id"] == 102
    assert recs[0]["similarity_score"] > recs[1]["similarity_score"]
    assert 0.0 <= recs[0]["similarity_score"] <= 1.0


def test_recommender_artifacts_save_and_load(fitted_toy_recommender, tmp_path):
    rec = fitted_toy_recommender
    save_dir = str(tmp_path / "model_test")
    rec.save_artifacts(output_dir=save_dir)

    assert os.path.exists(os.path.join(save_dir, "movie_metadata.parquet"))
    assert os.path.exists(os.path.join(save_dir, "count_vectorizer.joblib"))
    assert os.path.exists(os.path.join(save_dir, "feature_matrix.npz"))

    loaded_rec = ContentBasedRecommender.load_artifacts(artifact_dir=save_dir)
    assert len(loaded_rec.movies_df) == len(rec.movies_df)
    recs = loaded_rec.recommend(101, top_k=1)
    assert len(recs) == 1
    assert recs[0]["movie_id"] == 102
