"""
CineMatch — Training Pipeline CLI
Builds and saves production-ready recommendation model artifacts from raw TMDB data.

Usage:
    python -m src.train
    python src/train.py --output-dir models/
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
import pandas as pd

from src.data_loader import load_raw_tmdb_data
from src.preprocessing import preprocess_tmdb_metadata
from src.feature_engineering import build_movie_tags
from src.recommender import ContentBasedRecommender


def run_pipeline(
    movies_path: str = "data/raw/tmdb_5000_movies.csv",
    credits_path: str = "data/raw/tmdb_5000_credits.csv",
    output_dir: str = "models",
    max_features: int = 5000,
    apply_stemming: bool = True,
    merge_on: str = "id",
) -> None:
    """Execute end-to-end model building and artifact serialization."""
    start_time = time.time()
    print("=" * 65)
    print(" CineMatch — Training Pipeline: TMDB Content-Based Recommender")
    print("=" * 65)

    print(f"[*] Step 1: Loading raw datasets (merge_on='{merge_on}')...")
    df_raw = load_raw_tmdb_data(
        movies_path=movies_path,
        credits_path=credits_path,
        merge_on=merge_on,
    )
    print(f"    Raw records loaded: {len(df_raw)} rows, {df_raw.shape[1]} columns")

    print("[*] Step 2: Preprocessing structured metadata (JSON parsing & space collapse)...")
    df_clean = preprocess_tmdb_metadata(
        df_raw,
        drop_null_overview=True,
        cast_top_k=3,
    )
    print(f"    Cleaned records: {len(df_clean)} rows")

    print(f"[*] Step 3: Feature engineering tags (Stemming={apply_stemming})...")
    df_featured = build_movie_tags(df_clean, apply_stemming=apply_stemming)
    sample_tags = df_featured.iloc[0]["tags"][:120]
    print(f"    Sample tags preview: '{sample_tags}...'")

    print(f"[*] Step 4: Vectorizing with CountVectorizer (max_features={max_features})...")
    recommender = ContentBasedRecommender(
        max_features=max_features,
        stop_words="english",
    )
    recommender.fit(df_featured)

    nnz = recommender.feature_matrix.nnz
    total_elements = recommender.feature_matrix.shape[0] * recommender.feature_matrix.shape[1]
    sparsity = 100.0 * (1.0 - nnz / total_elements)
    print(f"    Feature matrix shape: {recommender.feature_matrix.shape}")
    print(f"    Non-zero entries: {nnz} (Sparsity: {sparsity:.2f}%)")

    print(f"[*] Step 5: Serializing artifacts to '{output_dir}/'...")
    paths = recommender.save_artifacts(output_dir=output_dir)

    # Validate model with a test query (e.g. 'The Dark Knight' or 'Gandhi')
    test_title = "The Dark Knight" if "the dark knight" in recommender._title_to_indices else df_featured.iloc[0]["title"]
    sample_recs = recommender.recommend(test_title, top_k=5)
    sample_rec_titles = [r["title"] for r in sample_recs]
    print(f"[*] Step 6: Verification Query for '{test_title}':")
    for rank, rec in enumerate(sample_recs, 1):
        print(f"    {rank}. {rec['title']} ({rec['release_year']}) — Similarity: {rec['similarity_percentage']}%")

    # Save training metadata
    meta_info = {
        "timestamp": datetime.now().isoformat(),
        "dataset_rows": len(df_featured),
        "vocabulary_size": len(recommender.vectorizer.vocabulary_),
        "max_features": max_features,
        "stemming_applied": apply_stemming,
        "merge_strategy": merge_on,
        "matrix_shape": list(recommender.feature_matrix.shape),
        "matrix_sparsity_percent": round(sparsity, 2),
        "test_query": test_title,
        "test_recommendations": sample_rec_titles,
        "build_duration_seconds": round(time.time() - start_time, 2),
    }
    meta_path = os.path.join(output_dir, "training_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, indent=2)

    print(f"[+] Training completed successfully in {meta_info['build_duration_seconds']}s!")
    print(f"    Artifacts saved:")
    for name, p in paths.items():
        size_kb = os.path.getsize(p) / 1024
        print(f"    - {name}: {p} ({size_kb:.1f} KB)")
    print(f"    - metadata: {meta_path}")
    print("=" * 65)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CineMatch Content-Based Recommender")
    parser.add_argument("--raw-movies", type=str, default="data/raw/tmdb_5000_movies.csv")
    parser.add_argument("--raw-credits", type=str, default="data/raw/tmdb_5000_credits.csv")
    parser.add_argument("--output-dir", type=str, default="models")
    parser.add_argument("--max-features", type=int, default=5000)
    parser.add_argument("--no-stemming", action="store_true", help="Disable Porter stemming")
    parser.add_argument("--merge-on", type=str, default="id", choices=["id", "title"])

    args = parser.parse_args()
    run_pipeline(
        movies_path=args.raw_movies,
        credits_path=args.raw_credits,
        output_dir=args.output_dir,
        max_features=args.max_features,
        apply_stemming=not args.no_stemming,
        merge_on=args.merge_on,
    )
