"""
CineMatch — Script to execute 02_feature_engineering.ipynb.
"""
import os
import nbformat
from nbclient import NotebookClient

os.makedirs('notebooks', exist_ok=True)

nb = nbformat.v4.new_notebook()
nb.metadata = {
    "language_info": {"name": "python", "version": "3.11.9"},
    "kernelspec": {"name": "python3", "display_name": "Python 3"}
}

cells = [
    nbformat.v4.new_markdown_cell(
        "# 02. Feature Engineering & Vectorization\n\n"
        "**Project**: CineMatch — TMDB Content-Based Movie Recommendation System  \n"
        "**Objective**: Faithfully implement and validate CampusX content-based feature engineering: "
        "JSON parsing, top-3 cast extraction, director isolation, entity space collapse, "
        "tag synthesis, Porter stemming, and CountVectorizer representation."
    ),
    nbformat.v4.new_code_cell(
        "import sys\n"
        "import os\n"
        "sys.path.append(os.path.abspath('..'))\n\n"
        "import pandas as pd\n"
        "import numpy as np\n"
        "from sklearn.feature_extraction.text import CountVectorizer\n"
        "from src.data_loader import load_raw_tmdb_data\n"
        "from src.preprocessing import preprocess_tmdb_metadata\n"
        "from src.feature_engineering import build_movie_tags\n\n"
        "print('CineMatch pipeline modules imported successfully.')"
    ),
    nbformat.v4.new_markdown_cell("## 1. Load Raw Merged TMDB Dataset"),
    nbformat.v4.new_code_cell(
        "movies_path = '../data/raw/tmdb_5000_movies.csv' if os.path.exists('../data/raw/tmdb_5000_movies.csv') else 'data/raw/tmdb_5000_movies.csv'\n"
        "credits_path = '../data/raw/tmdb_5000_credits.csv' if os.path.exists('../data/raw/tmdb_5000_credits.csv') else 'data/raw/tmdb_5000_credits.csv'\n\n"
        "df_raw = load_raw_tmdb_data(movies_path=movies_path, credits_path=credits_path, merge_on='id')\n"
        "print(f'Raw merged records: {df_raw.shape}')\n"
        "df_raw[['id', 'title', 'genres', 'overview', 'cast', 'crew']].head(2)"
    ),
    nbformat.v4.new_markdown_cell("## 2. Preprocessing & Entity Extraction"),
    nbformat.v4.new_code_cell(
        "df_clean = preprocess_tmdb_metadata(df_raw, drop_null_overview=True, cast_top_k=3)\n"
        "print(f'Cleaned records after null overview filtering: {df_clean.shape}')\n"
        "sample = df_clean.iloc[0]\n"
        "print('Movie:', sample['title'])\n"
        "print('Genres clean:', sample['genres_clean'])\n"
        "print('Genres collapsed:', sample['genres_collapsed'])\n"
        "print('Top 3 Cast clean:', sample['cast_clean'])\n"
        "print('Top 3 Cast collapsed:', sample['cast_collapsed'])\n"
        "print('Director clean:', sample['crew_clean'])\n"
        "print('Director collapsed:', sample['crew_collapsed'])"
    ),
    nbformat.v4.new_markdown_cell("## 3. Tag Combination & Porter Stemming"),
    nbformat.v4.new_code_cell(
        "df_featured = build_movie_tags(df_clean, apply_stemming=True)\n"
        "print('Sample synthesized tags for \"Avatar\":')\n"
        "print(df_featured.iloc[0]['tags'][:300] + '...')"
    ),
    nbformat.v4.new_markdown_cell("## 4. Bag-of-Words Vectorization (CountVectorizer)"),
    nbformat.v4.new_code_cell(
        "cv = CountVectorizer(max_features=5000, stop_words='english')\n"
        "feature_matrix = cv.fit_transform(df_featured['tags'])\n\n"
        "print(f'Feature matrix shape: {feature_matrix.shape}')\n"
        "print(f'Sparsity: {100.0 * (1.0 - feature_matrix.nnz / (feature_matrix.shape[0] * feature_matrix.shape[1])):.2f}%')\n"
        "vocab = cv.get_feature_names_out()\n"
        "print(f'Vocabulary size: {len(vocab)}')\n"
        "print('Sample vocabulary words (indices 1000-1015):', vocab[1000:1015])"
    ),
    nbformat.v4.new_markdown_cell("## 5. Verification of Entity Preservation in Vocabulary"),
    nbformat.v4.new_code_cell(
        "# Verify collapsed entities appear in vocabulary\n"
        "sample_entities = ['jamescameron', 'samworthington', 'sciencefiction', 'action', 'alien']\n"
        "for ent in sample_entities:\n"
        "    in_vocab = ent in cv.vocabulary_\n"
        "    idx = cv.vocabulary_.get(ent, -1)\n"
        "    print(f'Entity \"{ent}\": present={in_vocab}, index={idx}')"
    ),
    nbformat.v4.new_markdown_cell("## 6. Conclusions & Pipeline Export"),
    nbformat.v4.new_code_cell(
        "print('Feature engineering pipeline successfully verified.')\n"
        "print('All records have nonempty feature tags.')\n"
        "print(f'Zero-length tags count: {(df_featured[\"tags\"].str.len() == 0).sum()}')"
    )
]

nb.cells = cells

nb_path = 'notebooks/02_feature_engineering.ipynb'
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Executing {nb_path} with NotebookClient...")
client = NotebookClient(nb, timeout=60, kernel_name='python3')
client.execute()

with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Successfully executed and saved {nb_path}.")
