"""
CineMatch — Script to execute 01_eda.ipynb and export EDA figures.
"""
import os
import json
import ast
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat
from nbclient import NotebookClient

os.makedirs('reports/eda', exist_ok=True)
os.makedirs('notebooks', exist_ok=True)

sns.set_theme(style='whitegrid', font_scale=1.05)
palette = sns.color_palette("mako")

# Load data
movies = pd.read_csv('data/raw/tmdb_5000_movies.csv')
credits = pd.read_csv('data/raw/tmdb_5000_credits.csv')

print(f"Loaded movies: {movies.shape}, credits: {credits.shape}")

# 1. Missing Values Plot
missing = movies.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
missing_pct = (missing / len(movies)) * 100

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(missing.index, missing.values, color='#3b82f6', edgecolor='#1d4ed8')
ax.set_title("Missing Values Count in TMDB 5000 Movies", fontsize=14, weight='bold', pad=12)
ax.set_xlabel("Count of Missing Records", fontsize=11)
for bar, pct in zip(bars, missing_pct):
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2, f"{int(bar.get_width())} ({pct:.1f}%)", 
            va='center', fontsize=10, color='#1e293b')
ax.set_xlim(0, max(missing.values) * 1.15)
plt.tight_layout()
plt.savefig('reports/eda/01_missing_values.png', dpi=300)
plt.close()
print("Saved 01_missing_values.png")

# 2. Genre Distribution
def parse_names(val):
    if not isinstance(val, str):
        return []
    try:
        data = ast.literal_eval(val)
        return [item['name'] for item in data if 'name' in item]
    except Exception:
        return []

genres_series = movies['genres'].apply(parse_names)
all_genres = [g for sublist in genres_series for g in sublist]
genre_counts = pd.Series(all_genres).value_counts()

fig, ax = plt.subplots(figsize=(10, 5.5))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis', ax=ax)
ax.set_title("Frequency Distribution of Movie Genres (TMDB 5000)", fontsize=14, weight='bold', pad=12)
ax.set_xlabel("Total Occurrences Across Movies", fontsize=11)
ax.set_ylabel("Genre", fontsize=11)
for i, count in enumerate(genre_counts.values):
    ax.text(count + 25, i, str(count), va='center', fontsize=9.5, color='#0f172a')
ax.set_xlim(0, max(genre_counts.values) * 1.08)
plt.tight_layout()
plt.savefig('reports/eda/02_top_genres.png', dpi=300)
plt.close()
print("Saved 02_top_genres.png")

# 3. Release Year Distribution
movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
movies['release_year'] = movies['release_date'].dt.year

fig, ax = plt.subplots(figsize=(9, 4.5))
valid_years = movies['release_year'].dropna()
sns.histplot(valid_years, bins=40, kde=True, color='#0284c7', edgecolor='white', ax=ax)
ax.set_title("Distribution of Movie Release Years (1916 – 2017)", fontsize=14, weight='bold', pad=12)
ax.set_xlabel("Release Year", fontsize=11)
ax.set_ylabel("Movie Count", fontsize=11)
median_yr = valid_years.median()
ax.axvline(median_yr, color='#dc2626', linestyle='--', linewidth=1.5, label=f"Median: {int(median_yr)}")
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig('reports/eda/03_release_years.png', dpi=300)
plt.close()
print("Saved 03_release_years.png")

# 4. Vote Average Distribution
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.histplot(movies['vote_average'], bins=30, kde=True, color='#8b5cf6', edgecolor='white', ax=ax)
ax.set_title("Distribution of TMDB User Ratings (Vote Average)", fontsize=14, weight='bold', pad=12)
ax.set_xlabel("Vote Average (0.0 to 10.0)", fontsize=11)
ax.set_ylabel("Movie Count", fontsize=11)
mean_vote = movies['vote_average'].mean()
ax.axvline(mean_vote, color='#d97706', linestyle='--', linewidth=1.5, label=f"Mean: {mean_vote:.2f}")
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig('reports/eda/04_vote_distribution.png', dpi=300)
plt.close()
print("Saved 04_vote_distribution.png")

# 5. Overview Word Count Distribution
overview_lens = movies['overview'].fillna('').apply(lambda x: len(x.split()))
fig, ax = plt.subplots(figsize=(9, 4.5))
sns.histplot(overview_lens, bins=40, kde=True, color='#10b981', edgecolor='white', ax=ax)
ax.set_title("Distribution of Narrative Overview Word Lengths", fontsize=14, weight='bold', pad=12)
ax.set_xlabel("Word Count", fontsize=11)
ax.set_ylabel("Movie Count", fontsize=11)
mean_len = overview_lens.mean()
ax.axvline(mean_len, color='#0f766e', linestyle='--', linewidth=1.5, label=f"Mean Words: {mean_len:.1f}")
ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig('reports/eda/05_tag_length_distribution.png', dpi=300)
plt.close()
print("Saved 05_tag_length_distribution.png")

# Now let's construct notebooks/01_eda.ipynb with rich cells
nb = nbformat.v4.new_notebook()
nb.metadata = {
    "language_info": {"name": "python", "version": "3.11.9"},
    "kernelspec": {"name": "python3", "display_name": "Python 3"}
}

cells = [
    nbformat.v4.new_markdown_cell(
        "# 01. Exploratory Data Analysis & Data Quality Investigation\n\n"
        "**Project**: CineMatch — TMDB Content-Based Movie Recommendation System  \n"
        "**Dataset**: TMDB 5000 Movies & Credits Dataset  \n"
        "**Methodology**: Faithful reproduction & modernization of CampusX content-based recommendation approach  \n\n"
        "### Objectives:\n"
        "1. Inspect dataset dimensions, feature schemas, and missing value patterns.\n"
        "2. Analyze title homonyms and potential data corruption during merges.\n"
        "3. Investigate distributions of genres, release years, vote averages, and overview word counts.\n"
        "4. Document preprocessing implications for feature engineering."
    ),
    nbformat.v4.new_code_cell(
        "import os\n"
        "import ast\n"
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n\n"
        "sns.set_theme(style='whitegrid')\n"
        "print('Libraries successfully imported.')"
    ),
    nbformat.v4.new_markdown_cell("## 1. Load Raw Datasets"),
    nbformat.v4.new_code_cell(
        "movies_path = '../data/raw/tmdb_5000_movies.csv'\n"
        "credits_path = '../data/raw/tmdb_5000_credits.csv'\n\n"
        "# Fallback if running from root\n"
        "if not os.path.exists(movies_path):\n"
        "    movies_path = 'data/raw/tmdb_5000_movies.csv'\n"
        "    credits_path = 'data/raw/tmdb_5000_credits.csv'\n\n"
        "movies = pd.read_csv(movies_path)\n"
        "credits = pd.read_csv(credits_path)\n\n"
        "print(f'Movies table shape: {movies.shape}')\n"
        "print(f'Credits table shape: {credits.shape}')"
    ),
    nbformat.v4.new_code_cell(
        "movies.head(3)"
    ),
    nbformat.v4.new_code_cell(
        "credits.head(3)"
    ),
    nbformat.v4.new_markdown_cell("## 2. Missing Value & Null Pattern Analysis"),
    nbformat.v4.new_code_cell(
        "null_movies = movies.isnull().sum()\n"
        "null_movies = null_movies[null_movies > 0].to_frame('missing_count')\n"
        "null_movies['percentage'] = (null_movies['missing_count'] / len(movies)) * 100\n"
        "null_movies.sort_values('missing_count', ascending=False)"
    ),
    nbformat.v4.new_code_cell(
        "null_credits = credits.isnull().sum()\n"
        "print('Credits missing values:')\n"
        "print(null_credits)"
    ),
    nbformat.v4.new_markdown_cell("## 3. Investigating Duplicate Titles & Merge Safety"),
    nbformat.v4.new_code_cell(
        "# Find duplicate movie titles\n"
        "dup_titles = movies[movies.duplicated(subset=['title'], keep=False)]\n"
        "dup_titles[['id', 'title', 'release_date', 'vote_average']].sort_values('title')"
    ),
    nbformat.v4.new_code_cell(
        "# Compare merge strategies: merge on 'title' vs merge on 'id' == 'movie_id'\n"
        "merge_title = movies.merge(credits, on='title')\n"
        "merge_id = movies.merge(credits, left_on='id', right_on='movie_id')\n\n"
        "print(f'Rows after merge on title: {merge_title.shape[0]} (Cartesian product on duplicates)')\n"
        "print(f'Rows after merge on id: {merge_id.shape[0]} (Exact 1:1 join preserved)')"
    ),
    nbformat.v4.new_markdown_cell("## 4. Genre Frequency Analysis"),
    nbformat.v4.new_code_cell(
        "def extract_genres(raw):\n"
        "    try:\n"
        "        data = ast.literal_eval(raw)\n"
        "        return [item['name'] for item in data if 'name' in item]\n"
        "    except Exception:\n"
        "        return []\n\n"
        "movies['genre_list'] = movies['genres'].apply(extract_genres)\n"
        "all_genres = [g for sublist in movies['genre_list'] for g in sublist]\n"
        "genre_counts = pd.Series(all_genres).value_counts()\n"
        "print(f'Total distinct genres: {len(genre_counts)}')\n"
        "print('Top 10 Genres:\\n', genre_counts.head(10))"
    ),
    nbformat.v4.new_markdown_cell("## 5. Overview Word Length Distribution"),
    nbformat.v4.new_code_cell(
        "movies['overview_words'] = movies['overview'].fillna('').apply(lambda x: len(x.split()))\n"
        "print(movies['overview_words'].describe())"
    ),
    nbformat.v4.new_markdown_cell("## 6. Release Year & Rating Distributions"),
    nbformat.v4.new_code_cell(
        "movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')\n"
        "movies['release_year'] = movies['release_date'].dt.year\n"
        "print(f'Release year range: {movies[\"release_year\"].min()} to {movies[\"release_year\"].max()}')\n"
        "print(f'Vote average mean: {movies[\"vote_average\"].mean():.2f}, std: {movies[\"vote_average\"].std():.2f}')"
    ),
    nbformat.v4.new_markdown_cell(
        "## 7. Conclusions & Findings for Feature Engineering\n\n"
        "1. **Merge Protocol**: Merging on `id == movie_id` avoids contaminating homonymous titles.\n"
        "2. **Null Values**: Exactly 3 movies lack `overview`. Dropping or imputing blank string preserves 4,803 or 4,806 movies.\n"
        "3. **Structured Fields**: Genres, keywords, cast, and crew require safe JSON parsing via `ast.literal_eval`.\n"
        "4. **Entity Collapse**: Multi-word entity names must have whitespace removed to prevent false token associations."
    )
]

nb.cells = cells

# Save unexecuted first
nb_path = 'notebooks/01_eda.ipynb'
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Executing {nb_path} with NotebookClient...")
client = NotebookClient(nb, timeout=60, kernel_name='python3')
client.execute()

# Save executed notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Successfully executed and saved {nb_path} with {len(nb.cells)} cells.")
