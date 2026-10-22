# CineMatch: TMDB Content-Based Movie Recommendation System

**Academic Mini-Project Report**  
**Department of Computer Science & Engineering / Data Science**  
**Academic Year**: 2026  
**System**: CineMatch — Content-Based Movie Recommendation Engine  
**Methodological Reference**: CampusX (Nitish Singh) TMDB Movie Recommender  

---

## Abstract

With the exponential growth of global film streaming libraries, information overload poses a significant challenge to digital content discovery. Recommender systems mitigate this issue by navigating large media catalogs to surface relevant titles. This project implements **CineMatch**, an end-to-end, reproducible, content-based movie recommendation system built upon the canonical 5,000-movie The Movie Database (TMDB) dataset. Adhering to the vector space recommendation methodology popularized by CampusX, the system combines narrative overviews, genre classifications, plot keywords, top-three credited cast members, and the film director into unified semantic metadata tags. These textual documents are normalized via Porter stemming and transformed into a 5,000-dimensional Bag-of-Words feature space using Scikit-Learn's `CountVectorizer`. Recommendations are computed by determining pairwise cosine similarities across item feature vectors. 

To elevate the reference implementation to production-grade engineering standards, CineMatch resolves critical vulnerabilities present in earlier prototypes: eliminating hardcoded API keys, safely handling title homonyms via primary key relational joins, introducing compressed sparse matrix serialization to reduce artifact footprint from 185 MB to under 3 MB, and building a responsive Streamlit discovery interface with automated offline poster fallbacks. Empirical validation across 150 sampled queries demonstrates 100% self-exclusion compliance, 100% duplicate-free recommendation rankings, an average genre Jaccard similarity of 48.3%, and a sub-10 millisecond inference latency ($P_{95} = 9.31\text{ ms}$).

---

## 1. Introduction

Digital streaming and online entertainment platforms offer catalogs encompassing tens of thousands of films. While wide availability empowers audiences, users frequently encounter choice paralysis due to the difficulty of discovering movies aligned with their specific thematic tastes. Automated recommendation engines serve as the core discovery mechanism across modern platforms such as Netflix, Amazon Prime Video, and Disney+.

Recommendation algorithms broadly fall into two foundational paradigms:
1. **Collaborative Filtering**: Relies on user interaction matrices (ratings, clicks, watch duration) to identify latent behavioral correlations among clusters of users or items.
2. **Content-Based Filtering**: Relies strictly on the intrinsic metadata attributes of the items themselves (genres, directors, actors, synopses) to calculate geometric similarity between candidate items.

This project implements a modernized, production-ready content-based movie recommender system following the foundational curriculum developed by CampusX. By leveraging multi-field metadata extraction and vector space cosine similarity, CineMatch allows a user to select any movie in the TMDB catalog and immediately discover thematically, stylistically, and creatively resonant titles.

---

## 2. Problem Statement

Given a query movie $m_q \in \mathcal{M}$ selected by a user from a catalog of $N$ movies, the objective is to generate an ordered ranking of top-$K$ recommendations:
$$\mathcal{R}_K(m_q) = [m_1, m_2, \dots, m_K] \subset \mathcal{M} \setminus \{m_q\}$$
such that each recommended movie $m_k$ maximizes semantic and narrative content similarity to $m_q$, subject to:
1. **Self-Exclusion**: $m_q \notin \mathcal{R}_K(m_q)$.
2. **Idempotence and Determinism**: Re-querying the same movie yields consistent, identical rankings with robust tie-breaking.
3. **Low Latency**: Inference must execute in real time ($< 25\text{ ms}$) without retraining models on the fly.
4. **Resilience**: The system must operate seamlessly even when external services (e.g. poster image APIs) are inaccessible.

---

## 3. Objectives

1. **Faithful Reproduction**: Faithfully implement the core CampusX content-based recommendation methodology using TMDB movie metadata and cosine similarity.
2. **Data Quality Audit & Correction**: Identify and correct defects in legacy preprocessing (e.g. Cartesian product explosion from naive title joins).
3. **Modular Software Architecture**: Decouple data loading, preprocessing, feature engineering, vectorization, and interface rendering into reusable Python modules.
4. **Storage & Memory Optimization**: Eliminate heavy dense float64 matrix pickling in favor of efficient sparse matrix representations.
5. **Interactive UI/UX**: Build an intuitive Streamlit interface featuring film summaries, similarity percentage badges, director/cast credits, and explainable recommendation tags.
6. **Automated Verification**: Implement a 100% passing automated test suite covering unit operations, data parsing, poster fallbacks, and end-to-end inference.

---

## 4. Existing Approach and Related Work

Content-based filtering traces its roots to information retrieval and the vector space model formalized by Salton et al. In film recommendation, early systems relied on manual taxonomies or simple genre matching.

The reference implementation developed by CampusX (Nitish Singh) demonstrates how multiple heterogeneous metadata fields (cast, crew, genres, keywords, synopsis) can be harmonized into a single textual document and vectorized via `CountVectorizer`. While pedagogically outstanding, the original reference code suffered from several operational shortcomings:
- Hardcoded TMDB API authentication key committed to public version control.
- Inner join on movie titles rather than unique identifiers, leading to combinatorial cross-joining of homonymous movies (e.g. *Batman* 1989 vs. 1966).
- Full dense float64 similarity matrix serialization resulting in a 185 MB pickle file.
- Lack of error handling on missing poster images and network timeouts.
- Absence of unit testing and empirical validation diagnostics.

CineMatch retains the core content-based methodology while resolving each of these engineering deficiencies.

---

## 5. Dataset Description and Provenance

The project utilizes the canonical **TMDB 5000 Movie Dataset**, sourced originally from The Movie Database (TMDB) API via Kaggle.

### Constituent Tables:
1. **`tmdb_5000_movies.csv`** ($4,803$ rows, $20$ columns, $5.7\text{ MB}$):
   - Key attributes: `id`, `title`, `overview`, `genres`, `keywords`, `release_date`, `vote_average`, `vote_count`, `popularity`, `runtime`.
2. **`tmdb_5000_credits.csv`** ($4,803$ rows, $4$ columns, $40.0\text{ MB}$):
   - Key attributes: `movie_id`, `title`, `cast`, `crew`.

---

## 6. Exploratory Data Analysis & Quality Audit

Detailed exploratory data analysis was conducted in `notebooks/01_eda.ipynb` and documented in `docs/eda_findings.md`.

```
reports/eda/
├── 01_missing_values.png
├── 02_top_genres.png
├── 03_release_years.png
├── 04_vote_distribution.png
└── 05_tag_length_distribution.png
```

### Key Analytical Findings:
1. **Title Homonym Collision**:
   Three movie titles appear twice in the dataset:
   - *The Host* (2006, South Korea, Dir: Bong Joon-ho vs. 2013, USA, Dir: Andrew Niccol)
   - *Batman* (1989, Dir: Tim Burton vs. 1966, Dir: Leslie H. Martinson)
   - *Out of the Blue* (1980, Dir: Dennis Hopper vs. 2006, Dir: Robert Sarkies)
   *Impact*: Merging on `title` produces a Cartesian product ($2 \times 2 = 4$ rows per pair), expanding the dataset by 6 spurious rows and cross-contaminating credits. CineMatch resolves this by joining strictly on primary key `id == movie_id`.
2. **Missingness in Overview**: Exactly 3 movies lacked an overview string (`To Be Frank, Sinatra at 100`, `The Mongol King`, `Chiamatemi Francesco`). Following CampusX protocol, dropping these yields 4,800 active films.
3. **Genre Hierarchy**: The most prevalent genres across the catalog are Drama (2,297), Comedy (1,722), Thriller (1,274), and Action (1,154).
4. **Rating Distribution**: User ratings (`vote_average`) exhibit a Gaussian profile centered at $\mu = 6.09$, $\sigma = 1.19$.
5. **Lexical Density**: Film overviews have an average length of $54.2 \pm 31.8$ words, providing substantial vocabulary for Bag-of-Words modeling.

---

## 7. Preprocessing & Entity Disambiguation

Structured attributes in the TMDB dataset are serialized as JSON strings representing lists of dictionaries. The preprocessing pipeline (`src/preprocessing.py`) executes:

1. **Safe JSON Parsing**: Uses `ast.literal_eval` enclosed in defensive try-except blocks.
2. **Lead Actor Extraction**: Slices the top 3 billed cast members (`order: 0, 1, 2`) to prioritize stars over minor extras.
3. **Director Isolation**: Filters the crew array specifically for `job == 'Director'`.
4. **Entity Space Collapse**:
   $$\text{"Sam Worthington"} \longrightarrow \text{"SamWorthington"}$$
   $$\text{"Sam Mendes"} \longrightarrow \text{"SamMendes"}$$
   This transformation prevents token ambiguity in standard unigram tokenizers, ensuring that distinct individuals sharing a first name do not create false co-occurrence links.

---

## 8. Feature Engineering & Vector Space Representation

The feature synthesis pipeline (`src/feature_engineering.py`) constructs a single document for each movie:
$$\text{tags}_i = \text{tokens}(\text{overview}_i) + \text{genres}_i + \text{keywords}_i + \text{cast}_i + \text{crew}_i$$

1. **Morphological Stemming**:
   Tokens are processed with the Porter Stemmer (`nltk.stem.porter.PorterStemmer`), reducing words to their roots (e.g. `danced` $\rightarrow$ `danc`, `spacecraft` $\rightarrow$ `spacecraft`).
2. **CountVectorizer Bag-of-Words**:
   The documents are vectorized into a term-document matrix:
   $$\mathbf{X} \in \mathbb{R}^{N \times V}, \quad N = 4,800, \quad V = 5,000$$
   - Vocabulary restricted to the top 5,000 unigrams.
   - Standard English stopwords removed.
   - Sparsity: $99.39\%$ of matrix entries are zero.

---

## 9. Cosine Similarity Recommendation Engine

Cosine similarity computes the normalized dot product between two vector representations:
$$\text{Sim}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \frac{\sum_{k=1}^V u_k v_k}{\sqrt{\sum_{k=1}^V u_k^2} \sqrt{\sum_{k=1}^V v_k^2}}$$

### Algorithmic Properties:
- Invariant to document length: Two movies with differing narrative lengths are compared purely on relative term frequency distribution.
- Bounds: $\text{Sim}(\mathbf{u}, \mathbf{v}) \in [0.0, 1.0]$ for non-negative Bag-of-Words vectors.
- Diagonal: $\text{Sim}(\mathbf{u}, \mathbf{u}) = 1.0$. The query item is explicitly set to $-1.0$ prior to sorting to guarantee self-exclusion.

### Real-Time Inference Optimization:
Rather than storing a 185 MB dense similarity matrix, CineMatch retains the sparse matrix in memory and performs sparse-dense dot products on demand via `np.argpartition` and `np.lexsort`. This reduces memory overhead by 98% and achieves query latencies under 8 milliseconds.

---

## 10. System Architecture

```text
+-----------------------------------------------------------+
|                   Streamlit User Interface               |
|  [Movie Dropdown]  [K-Slider]  [Poster Cards]  [Why Tags] |
+-----------------------------+-----------------------------+
                              |
                              v
+-----------------------------------------------------------+
|              CineMatch Recommendation Engine              |
|        (src/recommender.py & src/poster.py)              |
+-----------------------------+-----------------------------+
                              |
        +---------------------+---------------------+
        |                                           |
        v                                           v
+-----------------------+               +-----------------------+
|    Model Artifacts    |               |    TMDB Poster API    |
| - movie_metadata.pqt  |               |  (Optional API Key    |
| - feature_matrix.npz  |               |  & SVG Local Fallback)|
| - vectorizer.joblib   |               +-----------------------+
+-----------------------+
        ^
        |
+-----------------------------------------------------------+
|                   Offline Training Pipeline               |
|            python -m src.train (src/train.py)             |
|   data/raw/tmdb_5000_*.csv -> Preprocessing -> Features   |
+-----------------------------------------------------------+
```

---

## 11. Implementation Details

- **Language & Runtime**: Python 3.11.9
- **Core Dependencies**: Scikit-Learn 1.8+, Pandas 2.3+, NumPy 2.4+, NLTK 3.10+, Streamlit 1.59+, Pytest 9.1+
- **Artifact Formats**:
  - `models/movie_metadata.parquet`: High-compression columnar storage for titles, overviews, and credits.
  - `models/feature_matrix.npz`: Scipy Compressed Sparse Row (CSR) matrix.
  - `models/count_vectorizer.joblib`: Pickled Scikit-Learn vectorizer.
  - `models/training_metadata.json`: Audit log of training timestamps, vocabulary sizes, and sparsity.

---

## 12. Verification & Automated Testing

The automated test suite (`tests/`) contains 20 comprehensive unit, integration, and smoke tests executed via Pytest:

```text
tests/test_data_loader.py::test_load_raw_tmdb_data_success PASSED        [  5%]
tests/test_data_loader.py::test_load_raw_tmdb_data_missing_file PASSED   [ 10%]
tests/test_data_loader.py::test_load_raw_tmdb_data_missing_column PASSED [ 15%]
tests/test_feature_engineering.py::test_stem_text PASSED                 [ 20%]
tests/test_feature_engineering.py::test_build_movie_tags PASSED          [ 25%]
tests/test_pipeline_e2e.py::test_production_artifacts_exist PASSED       [ 30%]
tests/test_pipeline_e2e.py::test_production_recommender_inference PASSED [ 35%]
tests/test_pipeline_e2e.py::test_production_recommender_query_avatar PASSED [ 40%]
tests/test_poster.py::test_fallback_svg_generation PASSED                [ 45%]
tests/test_poster.py::test_poster_url_fallback_when_no_api_key PASSED    [ 50%]
tests/test_poster.py::test_attribution_text PASSED                       [ 55%]
tests/test_preprocessing.py::test_extract_names_valid PASSED             [ 60%]
tests/test_preprocessing.py::test_extract_names_empty_and_invalid PASSED [ 65%]
tests/test_preprocessing.py::test_extract_top_cast PASSED                [ 70%]
tests/test_preprocessing.py::test_extract_director PASSED                [ 75%]
tests/test_preprocessing.py::test_collapse_spaces PASSED                 [ 80%]
tests/test_preprocessing.py::test_preprocess_tmdb_metadata PASSED        [ 85%]
tests/test_recommender.py::test_recommender_get_index PASSED             [ 90%]
tests/test_recommender.py::test_recommender_recommendation_logic PASSED  [ 95%]
tests/test_recommender.py::test_recommender_artifacts_save_and_load PASSED [100%]

============================= 20 passed in 3.33s ==============================
```

---

## 13. Results and Empirical Diagnostics

Empirical evaluation conducted via `src/evaluate.py` across 150 randomly sampled test queries yielded:

| Evaluation Metric | Measured Result | Interpretation |
|---|---|---|
| **Self-Exclusion Rate** | 100.0% | Query movie is never recommended to itself. |
| **Duplicate-Free Rate** | 100.0% | Every recommendation list contains distinct movies. |
| **Score Validity Rate** | 100.0% | All similarity scores strictly adhere to $0.0 \le S \le 1.0$. |
| **Mean Genre Jaccard Overlap** | 0.4827 | Approximately 48.3% genre consistency with query title. |
| **Sampled Catalog Coverage** | 11.98% (575 unique titles) | High exploration diversity across catalog. |
| **Mean Recommendation Latency** | 7.17 ms | Real-time response capability ($P_{95} = 9.31\text{ ms}$). |

### Illustrative Test Case:
- **Query**: *The Dark Knight* (2008, Dir: Christopher Nolan)
  1. *The Dark Knight Rises* (2012) — 42.3% match
  2. *Batman Begins* (2005) — 40.2% match
  3. *Batman Returns* (1992) — 33.1% match
  4. *Batman Forever* (1995) — 29.4% match
  5. *Batman* (1989) — 26.1% match

---

## 14. Scientific Limitations

1. **Absence of User Feedback Loop**: Recommendations depend entirely on movie metadata, unable to learn from individual user histories, skips, or watch times.
2. **Filter Bubble / Homogeneity**: Highly similar items within the same franchise dominate recommendations, occasionally hindering serendipitous discovery.
3. **Item Cold-Start**: Films with sparse overviews or unknown directors receive few unigram matches, leading to lower recommendation frequency.
4. **Quality Agnosticism**: Cosine similarity measures textual proximity, not cinematic quality. A low-rated film with identical plot keywords can score higher than an acclaimed masterpiece.

---

## 15. Conclusion

The CineMatch project successfully reproduces and modernizes the CampusX TMDB movie recommendation methodology. By applying disciplined software engineering, defensive data preprocessing, memory-efficient sparse serialization, and responsive UI design, the platform achieves real-time inference latency under 8 milliseconds and 100% test compliance. The resulting system serves as a robust educational benchmark and practical demonstration of vector space content-based filtering.

---

## 16. Future Scope

1. **Hybrid Blending**: Integrate collaborative filtering embeddings (e.g. Matrix Factorization or LightFM) with content similarity vectors.
2. **Sub-linear Search**: Implement approximate nearest neighbor (ANN) search (e.g. FAISS or HNSW) to scale similarity queries to catalogs with millions of titles.
3. **Semantic Embeddings**: Compare traditional Bag-of-Words against sentence transformers (e.g. `all-MiniLM-L6-v2`) for rich semantic nuance.
4. **Interactive User Feedback**: Allow users to like or dislike specific recommendations in real time to adapt candidate reranking dynamically.

---

## 17. References

1. CampusX (Nitish Singh), *Movie Recommender System using TMDB Dataset*, GitHub: `https://github.com/campusx-official/movie-recommender-system-tmdb-dataset`.
2. Salton, G., Wong, A., & Yang, C. S. (1975). *A vector space model for automatic indexing*. Communications of the ACM, 18(11), 613-620.
3. Ricci, F., Rokach, L., & Shapira, B. (2015). *Recommender Systems Handbook*. Springer.
4. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
5. The Movie Database (TMDB) API Documentation: `https://developer.themoviedb.org/reference/intro`.
