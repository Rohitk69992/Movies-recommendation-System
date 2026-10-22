"""
CineMatch — TMDB Content-Based Movie Recommendation System
Interactive Streamlit Application based on the CampusX methodology.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from src.recommender import ContentBasedRecommender
from src.poster import get_poster_url, get_tmdb_attribution_text
from src.train import run_pipeline

# Configure Streamlit Page
st.set_page_config(
    page_title="CineMatch — TMDB Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished, elegant UI
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    
    .badge-genre {
        background-color: #3b82f6;
        color: #ffffff;
    }
    
    .badge-year {
        background-color: #334155;
        color: #e2e8f0;
    }
    
    .badge-rating {
        background-color: #f59e0b;
        color: #ffffff;
    }
    
    .badge-score {
        background-color: #10b981;
        color: #ffffff;
        font-size: 0.85rem;
        padding: 3px 8px;
        border-radius: 6px;
    }
    
    .rec-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .rec-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #cbd5e1;
    }
    
    .rec-title {
        font-size: 1.0rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 8px;
        margin-bottom: 4px;
        line-height: 1.25;
        min-height: 2.5rem;
    }
    
    .rec-meta {
        font-size: 0.8rem;
        color: #64748b;
        margin-bottom: 6px;
    }
    
    .common-tag {
        display: inline-block;
        background-color: #f1f5f9;
        color: #475569;
        font-size: 0.72rem;
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    
    .attribution-footer {
        font-size: 0.8rem;
        color: #94a3b8;
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
        margin-top: 3rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading CineMatch recommendation engine...")
def load_recommender() -> ContentBasedRecommender:
    """Load model artifacts with auto-build fallback."""
    artifact_dir = "models"
    meta_path = os.path.join(artifact_dir, "movie_metadata.parquet")
    matrix_path = os.path.join(artifact_dir, "feature_matrix.npz")

    if not os.path.exists(meta_path) or not os.path.exists(matrix_path):
        with st.spinner("Building model artifacts from raw TMDB dataset..."):
            run_pipeline(output_dir=artifact_dir)

    return ContentBasedRecommender.load_artifacts(artifact_dir=artifact_dir)


# Load Recommender
try:
    recommender = load_recommender()
    movies_df = recommender.movies_df
except Exception as e:
    st.error(f"Error initializing recommender: {e}")
    st.stop()


# Sidebar Navigation & Settings
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&auto=format&fit=crop&q=60", use_container_width=True)
    st.title("🎬 CineMatch")
    st.caption("TMDB Content-Based Movie Recommender")
    st.markdown("---")

    st.subheader("⚙️ Recommendation Settings")
    top_k = st.slider("Number of Recommendations (K)", min_value=3, max_value=10, value=5, step=1)
    show_explanations = st.checkbox("Show Similarity Explanations", value=True)

    st.markdown("---")
    st.subheader("🔑 Poster API Status")
    api_key_present = bool(os.getenv("TMDB_API_KEY", "").strip())
    if api_key_present:
        st.success("✅ TMDB API Key Active")
    else:
        st.info("ℹ️ Using Local Card Fallbacks (Add `TMDB_API_KEY` in `.env` for official posters)")

    st.markdown("---")
    st.markdown(
        """
        **Methodology**:
        - Metadata: Genres, Keywords, Cast (top 3), Director, Overview
        - Vectorizer: `CountVectorizer(5000)`
        - Metric: Cosine Similarity
        - Dataset: TMDB 5000 Movies
        """
    )


# App Header
st.markdown("<div class='main-header'>CineMatch — Movie Recommendation Engine</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Discover films sharing themes, directors, actors, and storytelling motifs using Vector Space Cosine Similarity.</div>", unsafe_allow_html=True)

# Tabs
tab_recommender, tab_eda, tab_methodology, tab_about = st.tabs([
    "🎯 Movie Discovery",
    "📊 Dataset Insights & EDA",
    "📐 How It Works (Methodology)",
    "ℹ️ Project Specs"
])


# ==========================================
# TAB 1: MOVIE DISCOVERY & RECOMMENDER
# ==========================================
with tab_recommender:
    # Prepare title selection list (sorted alphabetically)
    titles_list = sorted(movies_df["title"].unique())

    # Default to an iconic reference title if present
    default_idx = 0
    default_candidates = ["The Dark Knight", "Inception", "Avatar", "Gandhi", "The Avengers"]
    for cand in default_candidates:
        if cand in titles_list:
            default_idx = titles_list.index(cand)
            break

    selected_title = st.selectbox(
        "Search or select a movie from the catalog:",
        titles_list,
        index=default_idx,
        help="Type to search through all 4,800 TMDB movies."
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        find_btn = st.button("🚀 Recommend Similar Movies", type="primary", use_container_width=True)

    # Resolve Query Movie
    try:
        query_idx = recommender.get_movie_index(selected_title)
        query_row = movies_df.iloc[query_idx]
        query_movie_id = int(query_row["movie_id"])
        query_year = int(query_row.get("release_year", 0))
        query_genres = query_row.get("genres_clean", [])
        if not isinstance(query_genres, list):
            query_genres = []
        query_director = query_row.get("crew_clean", ["Unknown"])
        query_director = query_director[0] if (isinstance(query_director, list) and query_director) else "Unknown"
        query_cast = query_row.get("cast_clean", [])
        if not isinstance(query_cast, list):
            query_cast = []
        query_vote = float(query_row.get("vote_average", 0.0))
        query_overview = str(query_row.get("overview_display", query_row.get("overview", "")))
        query_poster = get_poster_url(query_movie_id, title=selected_title)

        # Query Movie Hero Card
        st.markdown("### 📽️ Selected Film Profile")
        with st.container():
            col_hero_img, col_hero_info = st.columns([1, 3])
            with col_hero_img:
                st.image(query_poster, use_container_width=True, caption=f"ID: {query_movie_id}")
            with col_hero_info:
                st.markdown(f"<div class='hero-title'>{selected_title} ({query_year if query_year > 0 else 'N/A'})</div>", unsafe_allow_html=True)
                
                # Badges
                badges_html = f"<span class='badge badge-rating'>★ {query_vote:.1f} / 10</span>"
                for g in query_genres[:4]:
                    badges_html += f"<span class='badge badge-genre'>{g}</span>"
                st.markdown(badges_html, unsafe_allow_html=True)

                st.markdown(f"**🎬 Director:** {query_director}")
                st.markdown(f"**🌟 Starring:** {', '.join(query_cast) if query_cast else 'N/A'}")
                st.markdown(f"**📝 Synopsis:** {query_overview}")

        st.markdown("---")

        # Generate & Display Recommendations
        st.markdown(f"### 🎯 Top {top_k} Recommended Titles for *{selected_title}*")
        recommendations = recommender.recommend(query_movie_id, top_k=top_k, exclude_self=True)

        if not recommendations:
            st.warning("No similar titles could be computed for this movie.")
        else:
            # Render recommendations in responsive columns
            num_cols = min(top_k, 5)
            cols = st.columns(num_cols)

            for i, rec in enumerate(recommendations):
                col_idx = i % num_cols
                with cols[col_idx]:
                    rec_poster = get_poster_url(rec["movie_id"], title=rec["title"])
                    st.image(rec_poster, use_container_width=True)
                    st.markdown(f"**{rec['title']}** ({rec['release_year']})")
                    st.markdown(f"<span class='badge-score'>{rec['similarity_percentage']}% Match</span> ★ {rec['vote_average']:.1f}", unsafe_allow_html=True)

                    if rec["genres"]:
                        st.caption("🎭 " + ", ".join(rec["genres"][:2]))
                    st.caption(f"🎬 Dir: {rec['director']}")

                    if show_explanations and rec["common_tags"]:
                        tags_html = " ".join([f"<span class='common-tag'>{t}</span>" for t in rec["common_tags"][:4]])
                        st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)

                    with st.expander("📖 Synopsis"):
                        st.write(rec["overview"])

    except Exception as e:
        st.error(f"Error computing recommendations: {e}")


# ==========================================
# TAB 2: DATASET INSIGHTS & EDA
# ==========================================
with tab_eda:
    st.markdown("### 📊 Exploratory Data Analysis & Data Quality")
    st.write(
        "Below are the verified empirical findings from our analysis of the 4,803 TMDB movies dataset."
    )

    eda_files = [
        ("reports/eda/01_missing_values.png", "Missing Values Summary", "Evaluation of nulls across all 20 columns. Note that only 3 movies lacked an overview, which were safely filtered."),
        ("reports/eda/02_top_genres.png", "Genre Frequency Distribution", "Drama, Comedy, Thriller, and Action are the most frequent genres across the catalog."),
        ("reports/eda/03_release_years.png", "Release Year Distribution (1916 – 2017)", "The majority of titles span from 1995 to 2016, with a median release year of 2005."),
        ("reports/eda/04_vote_distribution.png", "User Ratings Distribution", "Vote averages follow a normal distribution centered at 6.09 ± 1.19 on a 10-point scale."),
        ("reports/eda/05_tag_length_distribution.png", "Narrative Overview Word Counts", "Average movie overview contains 54.2 words, providing rich lexical density for CountVectorizer unigrams."),
    ]

    for img_path, title, desc in eda_files:
        if os.path.exists(img_path):
            st.subheader(title)
            st.image(img_path, use_container_width=True)
            st.caption(desc)
            st.markdown("---")


# ==========================================
# TAB 3: METHODOLOGY
# ==========================================
with tab_methodology:
    st.markdown("### 📐 Recommendation Methodology: CampusX Vector Space Approach")
    st.markdown(
        """
        The CineMatch recommendation engine faithfully adheres to the content-based methodology formulated by **CampusX**:
        
        #### 1. Metadata Feature Selection
        Only qualitative content-bearing attributes are combined:
        - **Overview**: Free-text narrative summary of the film premise.
        - **Genres**: Story categorization (e.g. Science Fiction, Adventure).
        - **Keywords**: Specific plot elements (e.g. time travel, superhero).
        - **Top 3 Cast**: Leading actors with billing order 0, 1, 2.
        - **Director**: The creative lead filtered from crew where `job == 'Director'`.

        #### 2. Space Collapse for Entity Disambiguation
        Multi-word names have internal whitespace removed:
        - `"Sam Worthington"` $\\rightarrow$ `"SamWorthington"`
        - `"Sam Mendes"` $\\rightarrow$ `"SamMendes"`
        This prevents false token co-occurrences in the Bag-of-Words vocabulary.

        #### 3. Porter Stemming & Bag-of-Words Vectorization
        All tokens are stemmed using the Porter Stemmer (`danced` $\\rightarrow$ `danc`, `aliens` $\\rightarrow$ `alien`), 
        then transformed via Scikit-Learn `CountVectorizer(max_features=5000, stop_words='english')`.

        #### 4. Cosine Similarity Formula
        Given query movie vector $\\mathbf{u}$ and candidate vector $\\mathbf{v}$:
        $$\\cos(\\mathbf{u}, \\mathbf{v}) = \\frac{\\mathbf{u} \\cdot \\mathbf{v}}{\\|\\mathbf{u}\\|_2 \\|\\mathbf{v}\\|_2} = \\frac{\\sum_{k=1}^V u_k v_k}{\\sqrt{\\sum_{k=1}^V u_k^2} \\sqrt{\\sum_{k=1}^V v_k^2}}$$

        - Values range from $0.0$ (completely orthogonal / zero shared vocabulary) to $1.0$ (identical tag distribution).
        - The query movie itself always scores $1.0$ and is excluded from the recommendation list.
        """
    )


# ==========================================
# TAB 4: ABOUT & SPECS
# ==========================================
with tab_about:
    st.markdown("### ℹ️ Project Specifications & System Details")
    st.markdown(
        """
        - **Project Name**: CineMatch — TMDB Content-Based Movie Recommendation System
        - **Reference**: [CampusX Movie Recommender System (GitHub)](https://github.com/campusx-official/movie-recommender-system-tmdb-dataset)
        - **Catalog Size**: 4,800 active films
        - **Vocabulary Size**: 5,000 top unigrams
        - **Framework**: Streamlit 1.59+, Scikit-Learn 1.8+, Pandas 2.3+
        - **License**: Educational MIT / Open Source
        """
    )


# Footer Attribution
st.markdown(
    f"""
    <div class='attribution-footer'>
        {get_tmdb_attribution_text()}<br>
        Built with Streamlit & Scikit-Learn • College ML Mini-Project 2026
    </div>
    """,
    unsafe_allow_html=True,
)
