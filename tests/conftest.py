"""
Pytest Fixtures for CineMatch TMDB Recommender Tests.
"""

import pytest
import pandas as pd


@pytest.fixture
def sample_raw_movies_df():
    """A small controlled fixture representing raw tmdb_5000_movies.csv."""
    return pd.DataFrame([
        {
            "id": 101,
            "title": "Space Odyssey",
            "overview": "An epic journey into deep space and artificial intelligence.",
            "genres": '[{"id": 878, "name": "Science Fiction"}, {"id": 12, "name": "Adventure"}]',
            "keywords": '[{"id": 1, "name": "space"}, {"id": 2, "name": "astronaut"}]',
            "release_date": "2001-04-02",
            "vote_average": 8.3,
            "vote_count": 5000,
        },
        {
            "id": 102,
            "title": "Solar Wind",
            "overview": "Astronauts battle rogue artificial intelligence on a distant moon.",
            "genres": '[{"id": 878, "name": "Science Fiction"}, {"id": 28, "name": "Action"}]',
            "keywords": '[{"id": 1, "name": "space"}, {"id": 3, "name": "robot"}]',
            "release_date": "2010-07-16",
            "vote_average": 7.9,
            "vote_count": 4200,
        },
        {
            "id": 103,
            "title": "Love in Paris",
            "overview": "A charming romance unfolds in the streets of Paris.",
            "genres": '[{"id": 10749, "name": "Romance"}, {"id": 35, "name": "Comedy"}]',
            "keywords": '[{"id": 4, "name": "paris"}, {"id": 5, "name": "love"}]',
            "release_date": "2015-02-14",
            "vote_average": 6.8,
            "vote_count": 1800,
        },
        {
            "id": 104,
            "title": "Silent Echo",
            "overview": None,  # Missing overview to test null handling
            "genres": '[{"id": 18, "name": "Drama"}]',
            "keywords": '[]',
            "release_date": "2020-01-01",
            "vote_average": 5.0,
            "vote_count": 50,
        }
    ])


@pytest.fixture
def sample_raw_credits_df():
    """A small controlled fixture representing raw tmdb_5000_credits.csv."""
    return pd.DataFrame([
        {
            "movie_id": 101,
            "title": "Space Odyssey",
            "cast": '[{"name": "Keir Dullea", "order": 0}, {"name": "Gary Lockwood", "order": 1}]',
            "crew": '[{"name": "Stanley Kubrick", "job": "Director"}, {"name": "Arthur C. Clarke", "job": "Writer"}]',
        },
        {
            "movie_id": 102,
            "title": "Solar Wind",
            "cast": '[{"name": "Keir Dullea", "order": 0}, {"name": "Sigourney Weaver", "order": 1}]',
            "crew": '[{"name": "Stanley Kubrick", "job": "Director"}]',
        },
        {
            "movie_id": 103,
            "title": "Love in Paris",
            "cast": '[{"name": "Audrey Tautou", "order": 0}]',
            "crew": '[{"name": "Jean-Pierre Jeunet", "job": "Director"}]',
        },
        {
            "movie_id": 104,
            "title": "Silent Echo",
            "cast": '[]',
            "crew": '[]',
        }
    ])
