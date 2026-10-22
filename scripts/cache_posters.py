"""
Script to pre-cache high-resolution TMDB posters locally for key catalog movies.
"""

import json
import os
import time
import urllib.request
from typing import Set

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY", "").strip()
POSTER_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "posters")
os.makedirs(POSTER_DIR, exist_ok=True)


def download_poster(movie_id: int) -> bool:
    target_path = os.path.join(POSTER_DIR, f"{movie_id}.jpg")
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        return True

    if not API_KEY:
        return False

    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        poster_path = data.get("poster_path")
        if not poster_path:
            return False

        img_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(img_req, timeout=8) as img_resp:
            img_data = img_resp.read()

        with open(target_path, "wb") as f:
            f.write(img_data)

        print(f"Downloaded poster for {movie_id} ({data.get('title')}) -> {len(img_data)} bytes")
        return True
    except Exception as e:
        print(f"Failed for {movie_id}: {e}")
        return False


def main():
    from src.recommender import ContentBasedRecommender
    rec = ContentBasedRecommender.load_artifacts("models")
    
    seed_titles = [
        "The Dark Knight", "Inception", "Avatar", "Interstellar", "The Avengers",
        "Gladiator", "Titanic", "Fight Club", "Pulp Fiction", "The Matrix",
        "The Godfather", "Deadpool", "The Shawshank Redemption", "Toy Story", 
        "Spider-Man", "Iron Man", "Batman Begins", "The Dark Knight Rises"
    ]

    ids_to_fetch: Set[int] = set()
    for title in seed_titles:
        try:
            idx = rec.get_movie_index(title)
            ids_to_fetch.add(int(rec.movies_df.iloc[idx]["movie_id"]))
            for r in rec.recommend(title, top_k=6):
                ids_to_fetch.add(int(r["movie_id"]))
        except Exception as e:
            print(f"Error resolving {title}: {e}")

    print(f"Found {len(ids_to_fetch)} unique movie IDs to cache.")
    success_count = 0
    for m_id in sorted(ids_to_fetch):
        if download_poster(m_id):
            success_count += 1
        time.sleep(0.05)  # Respectful rate limit

    print(f"Successfully cached {success_count} / {len(ids_to_fetch)} posters in {POSTER_DIR}")


if __name__ == "__main__":
    main()
