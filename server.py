"""
CineMatch — FastAPI Web Server
Serves both the REST API and the modern HTML5/CSS/JavaScript single-page application.
Runs on http://localhost:8000
"""

import os
from typing import Optional, List
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from src.recommender import ContentBasedRecommender, _ensure_list
from src.poster import (
    get_poster_url, 
    get_tmdb_attribution_text, 
    fetch_and_cache_poster, 
    generate_fallback_svg_raw
)
from src.train import run_pipeline

# Initialize FastAPI
app = FastAPI(
    title="CineMatch — TMDB Movie Recommender",
    description="Content-Based Movie Recommendation Engine based on CampusX Vector Space Methodology",
    version="2.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model Artifacts
ARTIFACT_DIR = "models"
recommender: Optional[ContentBasedRecommender] = None


def get_recommender() -> ContentBasedRecommender:
    """Lazy loader for recommender artifacts."""
    global recommender
    if recommender is None:
        meta_path = os.path.join(ARTIFACT_DIR, "movie_metadata.parquet")
        matrix_path = os.path.join(ARTIFACT_DIR, "feature_matrix.npz")
        if not os.path.exists(meta_path) or not os.path.exists(matrix_path):
            run_pipeline(output_dir=ARTIFACT_DIR)
        recommender = ContentBasedRecommender.load_artifacts(ARTIFACT_DIR)
    return recommender


# Mount Static Assets
os.makedirs("frontend/css", exist_ok=True)
os.makedirs("frontend/js", exist_ok=True)
os.makedirs("reports/eda", exist_ok=True)

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/reports/eda", StaticFiles(directory="reports/eda"), name="eda_reports")


@app.get("/")
def serve_index():
    """Serve the single-page application."""
    index_file = "frontend/index.html"
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "CineMatch API is running. frontend/index.html not found."}


@app.get("/api/movies")
def search_movies(
    q: str = Query("", description="Search substring for movie title"),
    limit: int = Query(15, ge=1, le=100),
):
    """
    Search and autocomplete movies by title prefix or substring.
    """
    rec = get_recommender()
    df = rec.movies_df

    if not q.strip():
        # Return popular curated sample
        sample_titles = [
            "The Dark Knight", "Inception", "Avatar", "Interstellar", 
            "The Avengers", "Titanic", "Fight Club", "Pulp Fiction",
            "Gladiator", "The Matrix", "Gandhi", "The Godfather"
        ]
        subset = df[df["title"].isin(sample_titles)]
        results = []
        for _, row in subset.iterrows():
            results.append({
                "movie_id": int(row["movie_id"]),
                "title": str(row["title"]),
                "release_year": int(row.get("release_year", 0)),
                "vote_average": float(row.get("vote_average", 0.0)),
                "genres": _ensure_list(row.get("genres_clean"))[:3],
            })
        return {"total": len(results), "movies": results}

    q_lower = q.strip().lower()
    matches = df[df["title"].str.lower().str.contains(q_lower, na=False)].head(limit)

    results = []
    for _, row in matches.iterrows():
        results.append({
            "movie_id": int(row["movie_id"]),
            "title": str(row["title"]),
            "release_year": int(row.get("release_year", 0)),
            "vote_average": float(row.get("vote_average", 0.0)),
            "genres": _ensure_list(row.get("genres_clean"))[:3],
        })

    return {"total": len(results), "movies": results}


@app.get("/api/poster/{movie_id}")
def get_movie_poster_image(movie_id: int):
    """
    Serve high-resolution movie poster image locally from disk or cache.
    Guarantees reliable image rendering in browser without ISP/CORS/Adblock blocks.
    """
    local_path = os.path.join("data", "posters", f"{movie_id}.jpg")
    if os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
        return FileResponse(local_path, media_type="image/jpeg")

    # Fetch from TMDB and cache to disk
    cached = fetch_and_cache_poster(movie_id)
    if cached and os.path.exists(cached) and os.path.getsize(cached) > 1000:
        return FileResponse(cached, media_type="image/jpeg")

    # Fallback to typographic editorial SVG
    title = "Feature Film"
    year = None
    genre = None
    try:
        rec = get_recommender()
        idx = rec.get_movie_index(movie_id)
        row = rec.movies_df.iloc[idx]
        title = str(row["title"])
        year = int(row.get("release_year", 0))
        genres = _ensure_list(row.get("genres_clean"))
        genre = genres[0] if genres else None
    except Exception:
        pass

    svg_content = generate_fallback_svg_raw(title=title, year=year, genre=genre)
    return Response(content=svg_content, media_type="image/svg+xml")


@app.get("/api/movie/{identifier}")
def get_movie_details(identifier: str):
    """
    Get full metadata and poster for a specific movie ID or title.
    """
    rec = get_recommender()
    try:
        idx = rec.get_movie_index(identifier)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Movie '{identifier}' not found in catalog.")

    row = rec.movies_df.iloc[idx]
    m_id = int(row["movie_id"])
    title = str(row["title"])
    genres = _ensure_list(row.get("genres_clean"))
    cast = _ensure_list(row.get("cast_clean"))
    crew = _ensure_list(row.get("crew_clean"))
    director = crew[0] if crew else "Unknown"

    return {
        "movie_id": m_id,
        "title": title,
        "release_year": int(row.get("release_year", 0)),
        "genres": genres,
        "director": director,
        "top_cast": cast,
        "overview": str(row.get("overview_display", row.get("overview", ""))),
        "vote_average": float(row.get("vote_average", 0.0)),
        "vote_count": int(row.get("vote_count", 0)),
        "poster_url": get_poster_url(m_id, title=title, year=int(row.get("release_year", 0)), genre=genres[0] if genres else None),
    }


@app.get("/api/recommend/{identifier}")
def get_recommendations(
    identifier: str,
    top_k: int = Query(5, ge=1, le=20),
):
    """
    Compute top-K content-based recommendations for a query movie.
    """
    rec = get_recommender()
    try:
        query_idx = rec.get_movie_index(identifier)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Query movie '{identifier}' not found.")

    query_row = rec.movies_df.iloc[query_idx]
    query_id = int(query_row["movie_id"])
    query_title = str(query_row["title"])
    query_genres = _ensure_list(query_row.get("genres_clean"))
    query_year = int(query_row.get("release_year", 0))

    raw_recs = rec.recommend(query_id, top_k=top_k, exclude_self=True)

    enriched_recs = []
    for r in raw_recs:
        r_id = r["movie_id"]
        r_title = r["title"]
        r_genres = r.get("genres", [])
        r_year = r.get("release_year")
        r["poster_url"] = get_poster_url(
            r_id,
            title=r_title,
            year=r_year,
            genre=r_genres[0] if r_genres else None
        )
        enriched_recs.append(r)

    return {
        "query_movie": {
            "movie_id": query_id,
            "title": query_title,
            "release_year": query_year,
            "genres": query_genres,
            "director": _ensure_list(query_row.get("crew_clean"))[0] if _ensure_list(query_row.get("crew_clean")) else "Unknown",
            "top_cast": _ensure_list(query_row.get("cast_clean")),
            "overview": str(query_row.get("overview_display", query_row.get("overview", ""))),
            "vote_average": float(query_row.get("vote_average", 0.0)),
            "poster_url": get_poster_url(query_id, title=query_title, year=query_year, genre=query_genres[0] if query_genres else None),
        },
        "count": len(enriched_recs),
        "recommendations": enriched_recs,
        "attribution": get_tmdb_attribution_text(),
    }


@app.get("/api/stats")
def get_system_stats():
    """Return model, dataset, and system metadata."""
    rec = get_recommender()
    meta_path = os.path.join(ARTIFACT_DIR, "training_metadata.json")
    train_meta = {}
    if os.path.exists(meta_path):
        import json
        with open(meta_path, "r", encoding="utf-8") as f:
            train_meta = json.load(f)

    return {
        "catalog_size": len(rec.movies_df),
        "vocabulary_size": len(rec.vectorizer.vocabulary_) if rec.vectorizer else 5000,
        "matrix_shape": list(rec.feature_matrix.shape),
        "training_metadata": train_meta,
        "api_key_configured": bool(os.getenv("TMDB_API_KEY", "").strip()),
    }


if __name__ == "__main__":
    print("=" * 60)
    print(" Starting CineMatch Fast Web Server on http://localhost:8000")
    print("=" * 60)
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
