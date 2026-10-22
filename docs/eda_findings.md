# Exploratory Data Analysis & Data Quality Findings

**Project**: CineMatch — TMDB Content-Based Movie Recommendation System  
**Dataset**: TMDB 5000 Movies & Credits Dataset  
**Date**: October 22, 2026  
**Author**: Data Science & ML Engineering Team  

---

## 1. Dataset Dimensions and Overview

The canonical dataset consists of two relational tables:
- **`tmdb_5000_movies.csv`**: $4,803$ rows, $20$ columns.
- **`tmdb_5000_credits.csv`**: $4,803$ rows, $4$ columns.

### Schema Summary:
- **Identifier fields**: `id` in movies, `movie_id` in credits.
- **Text & Metadata fields**: `title`, `overview`, `genres`, `keywords`, `cast`, `crew`.
- **Numerical & Financial fields**: `budget`, `revenue`, `popularity`, `vote_average`, `vote_count`, `runtime`.
- **Temporal field**: `release_date`.

---

## 2. Data Quality Audit & Identified Anomalies

| Data Quality Issue | Affected Records | Proportion | Engineering Treatment Selected | Justification | Potential Information Loss |
|---|---|---|---|---|---|
| **Homonymous Titles (Duplicate Titles across Years)** | 6 rows (3 duplicate title pairs: *The Host*, *Batman*, *Out of the Blue*) | 0.12% of dataset | Perform relational merge strictly on primary key `id == movie_id` rather than on `title`. Disambiguate titles in UI using release year (e.g., *Batman (1989)* vs. *Batman (1966)*). | Merging on `title` produces a Cartesian product ($2 \times 2 = 4$ records per pair), resulting in spurious cross-contamination where Tim Burton's 1989 Batman is matched with Leslie Martinson's 1966 cast and crew. | Zero loss. Eliminates $6$ corrupt duplicate records caused by naive title merging. |
| **Missing Overview Summaries** | 3 rows (`id`: 380097, 370980, 459488) | 0.06% of dataset | Impute with empty string `""` or drop record if all metadata is missing. | In content-based modeling, an empty overview yields zero unigrams, but the movie may still possess genres and cast. For exact parity with the CampusX notebook, dropping these 3 rows results in 4,800 or 4,806 records. | Minimal text context for 3 obscure titles. |
| **Empty Structured Metadata Arrays** | 28 movies have `genres == '[]'`; 412 movies have `keywords == '[]'`; 43 have `cast == '[]'`; 28 have `crew == '[]'` | 0.58% to 8.58% | Safe parsing with `try-except` defaulting to `[]`. Fall back to available overview tokens. | Eliminates runtime parser crashes from `ast.literal_eval`. Ensures partial metadata is retained rather than discarding movies entirely. | Zero loss. Preserves discoverability of indie and documentary films. |
| **Missing Release Dates** | 1 row (`id`: 380097, *America Is Still the Place*) | 0.02% of dataset | Parse with `pd.to_datetime(..., errors='coerce')` defaulting to `Unknown Year`. | Does not impact content similarity calculation because release year is not an input feature in CampusX methodology. | Zero loss. |
| **Null Runtime** | 2 rows | 0.04% of dataset | Retained as `NaN` or median imputation (103 mins). | Runtime is excluded from content tags. | Zero loss. |
| **High Missingness in Ancillary Fields** | `homepage`: 3,091 nulls (64.4%); `tagline`: 844 nulls (17.6%) | 64.4% / 17.6% | Excluded from feature tags in accordance with CampusX methodology. | Neither field is used in the reference content-based feature representation. | Zero loss. |

---

## 3. Exploratory Distributions & Empirical Insights

### 3.1 Missing Values Across Columns
As shown in `reports/eda/01_missing_values.png`:
- `homepage` (3,091 missing) and `tagline` (844 missing) exhibit the highest missingness.
- In core content fields (`title`, `genres`, `keywords`, `cast`, `crew`), missingness is virtually $0\%$, with only $3$ movies missing narrative `overview`.

### 3.2 Genre Frequencies
As illustrated in `reports/eda/02_top_genres.png`:
- Total distinct genres identified: $20$.
- The top 5 dominant genres are:
  1. **Drama**: 2,297 occurrences
  2. **Comedy**: 1,722 occurrences
  3. **Thriller**: 1,274 occurrences
  4. **Action**: 1,154 occurrences
  5. **Romance**: 894 occurrences
- Niche genres include **Documentary** (110), **Foreign** (34), and **TV Movie** (8).
- Multi-label distribution: The average movie has $2.53$ associated genres.

### 3.3 Temporal Distribution of Releases
As illustrated in `reports/eda/03_release_years.png`:
- The dataset spans releases from $1916$ (*Intolerance*) to $2017$.
- Over $75\%$ of the movies were released between $1995$ and $2016$, reflecting the modern era of commercial cinema.
- Median release year is $2005$.

### 3.4 User Rating & Popularity Distribution
As illustrated in `reports/eda/04_vote_distribution.png`:
- Mean `vote_average` is $6.09 \pm 1.19$ on a 10-point scale.
- The distribution is bell-shaped with a slight negative skew.
- A small spike occurs at $0.0$ for unrated or obscure titles with $0$ vote count.

### 3.5 Text Length Analysis of Content Overviews
As illustrated in `reports/eda/05_tag_length_distribution.png`:
- The average `overview` length is $54.2 \pm 31.8$ words.
- Median length is $51$ words, providing sufficient lexical density for unigram CountVectorizer extraction.
- Shortest overview is $0$ words (3 movies); longest overview is $175$ words.

---

## 4. Key Preprocessing Decisions for CineMatch

1. **Relational Join Protocol**:
   Join `movies` and `credits` on `movies.id == credits.movie_id`. If `title` is duplicated, append the release year for unambiguous UI presentation (`title (year)`).

2. **Entity Space Collapse**:
   Actors and directors frequently share first or last names (e.g., "Sam Worthington" vs. "Sam Mendes", "Chris Evans" vs. "Chris Hemsworth"). Removing internal whitespace (`SamWorthington`, `SamMendes`) ensures the unigram `CountVectorizer` treats each person as a single atomic token.

3. **Top-3 Cast Selection**:
   The full cast array often contains 20+ minor characters, which introduces noise and dilutes recommendation focus. Retaining only the top 3 billed cast members concentrates similarity on lead actors.

4. **Director Extraction**:
   Among hundreds of crew roles (sound editors, visual effects, grips), only the `job == 'Director'` captures the overarching directorial style of the film.
