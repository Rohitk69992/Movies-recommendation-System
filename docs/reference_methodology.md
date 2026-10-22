# Reference Methodology Analysis: CampusX TMDB Movie Recommender System

## 1. Executive Summary & Attribution

This document provides a thorough audit and documentation of the reference implementation created by **CampusX**:
- **Repository**: [campusx-official/movie-recommender-system-tmdb-dataset](https://github.com/campusx-official/movie-recommender-system-tmdb-dataset)
- **Primary Files Inspected**:
  - `README.md`
  - `notebook86c26b4f17.ipynb` (40 code cells)
  - `app.py` (Streamlit 0.x legacy script)
- **Original Author**: CampusX (Nitish Singh)
- **Licensing & Attribution**: The reference project is an open-source educational demonstration created on Kaggle and GitHub for teaching content-based recommender systems. This project honors and preserves attribution while improving code quality, modularity, security, testing, and modern Python standards.

---

## 2. Dataset Provenance and Input Schemas

### 2.1 Dataset Source
The reference notebook specifies Kaggle's **TMDB 5000 Movie Dataset** (originating from The Movie Database API via Kaggle):
- Path in Kaggle environment: `/kaggle/input/tmdb-movie-metadata/`
- Constituent files:
  1. `tmdb_5000_movies.csv` (approx. 5,000 records, 20 columns)
  2. `tmdb_5000_credits.csv` (approx. 5,000 records, 4 columns)

### 2.2 Input Columns
- **`tmdb_5000_movies.csv`**:
  - `id`: Unique integer movie identifier in TMDB.
  - `title`: Movie release title.
  - `overview`: Free-text summary string.
  - `genres`: Serialized JSON array of dictionaries `[{"id": 28, "name": "Action"}, ...]`.
  - `keywords`: Serialized JSON array of dictionaries `[{"id": 1463, "name": "culture clash"}, ...]`.
  - Additional non-text columns (dropped by reference): `budget`, `homepage`, `original_language`, `original_title`, `popularity`, `production_companies`, `production_countries`, `release_date`, `revenue`, `runtime`, `spoken_languages`, `status`, `tagline`, `vote_average`, `vote_count`.
- **`tmdb_5000_credits.csv`**:
  - `movie_id`: Integer identifier matching `id` in `movies.csv`.
  - `title`: Movie title string.
  - `cast`: Serialized JSON array of dictionaries with cast members `[{"cast_id": ..., "character": ..., "credit_id": ..., "gender": ..., "id": ..., "name": "Sam Worthington", "order": 0}, ...]`.
  - `crew`: Serialized JSON array of dictionaries with crew members `[{"credit_id": ..., "department": ..., "gender": ..., "id": ..., "job": "Director", "name": "James Cameron"}, ...]`.

---

## 3. Reference Preprocessing & Data Cleaning Pipeline

In `notebook86c26b4f17.ipynb`, the preprocessing steps are:

1. **Table Merge**:
   ```python
   movies = movies.merge(credits, on='title')
   ```
   *Note*: The merge is performed on `title`. After merge, the dataset dimensions expand to $4809 \times 23$.

2. **Column Subsetting**:
   The notebook filters down to exactly 7 columns:
   ```python
   movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
   ```

3. **Handling Missing Values**:
   ```python
   movies.dropna(inplace=True)
   ```
   Drops the 3 rows with null `overview` values, yielding 4806 remaining movies.

4. **Parsing Serialized JSON Attributes (`ast.literal_eval`)**:
   - **`genres` & `keywords`**:
     ```python
     def convert(text):
         L = []
         for i in ast.literal_eval(text):
             L.append(i['name'])
         return L
     ```
     Extracts all genre names and keyword names into lists of strings.
   - **`cast`**:
     Keeps the top 3 billed actors:
     ```python
     def convert3(text):
         L = []
         counter = 0
         for i in ast.literal_eval(text):
             if counter < 3:
                 L.append(i['name'])
             counter += 1
         return L
     ```
     (Or parses all names with `convert()` and slices `x[0:3]`).
   - **`crew`**:
     Filters specifically for director:
     ```python
     def fetch_director(text):
         L = []
         for i in ast.literal_eval(text):
             if i['job'] == 'Director':
                 L.append(i['name'])
         return L
     ```

5. **Entity Disambiguation / Space Collapse**:
   To prevent token ambiguity in Bag-of-Words (e.g., distinguishing "Sam Worthington" from "Sam Mendes"), the reference collapses interior whitespace:
   ```python
   def collapse(L):
       L1 = []
       for i in L:
           L1.append(i.replace(" ", ""))
       return L1

   movies['cast'] = movies['cast'].apply(collapse)
   movies['crew'] = movies['crew'].apply(collapse)
   movies['genres'] = movies['genres'].apply(collapse)
   movies['keywords'] = movies['keywords'].apply(collapse)
   ```
   Result: `"Sam Worthington"` $\rightarrow$ `"SamWorthington"`, `"Science Fiction"` $\rightarrow$ `"ScienceFiction"`.

6. **Overview Tokenization**:
   ```python
   movies['overview'] = movies['overview'].apply(lambda x: x.split())
   ```

7. **Tag Concatenation**:
   ```python
   movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
   new = movies.drop(columns=['overview', 'genres', 'keywords', 'cast', 'crew'])
   new['tags'] = new['tags'].apply(lambda x: " ".join(x))
   ```

---

## 4. Vectorization and Similarity Computation

1. **Bag-of-Words Vectorization**:
   The reference utilizes `CountVectorizer` from Scikit-Learn:
   ```python
   from sklearn.feature_extraction.text import CountVectorizer
   cv = CountVectorizer(max_features=5000, stop_words='english')
   vector = cv.fit_transform(new['tags']).toarray()
   ```
   - Vocabulary size: 5,000 top unigrams.
   - Stopwords: English standard stopword list.
   - Output shape: $(4806, 5000)$ dense array (`.toarray()`).

2. **Stemming (Video vs. Notebook Note)**:
   In the recorded tutorial, CampusX demonstrates applying `nltk.stem.porter.PorterStemmer` so that tokens such as `"loved"`, `"loving"`, `"love"` map to `"love"`. In the committed notebook `notebook86c26b4f17.ipynb`, this was omitted in the final code cell or executed in a scratch cell. Our implementation provides full stemming support with optional toggle for strict adherence to the complete video methodology.

3. **Cosine Similarity**:
   ```python
   from sklearn.metrics.pairwise import cosine_similarity
   similarity = cosine_similarity(vector)
   ```
   - Computes dense $4806 \times 4806$ pairwise cosine matrix.
   - Storage in memory: $4806 \times 4806 \times 8 \text{ bytes} \approx 184.8 \text{ MB}$.

---

## 5. Recommendation Logic

```python
def recommend(movie):
    index = new[new['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].title)
```
- Query resolution: Finds integer index corresponding to `title == movie`.
- Enumerate & Sort: Pairs every movie index $j$ with similarity score $S(i, j)$, sorted descending.
- Top-K: Takes slice `[1:6]`, omitting position 0 (the query movie itself, where $S(i, i) = 1.0$).
- Output: Returns 5 movie titles.

---

## 6. Poster Retrieval & Streamlit Interface (`app.py`)

In `app.py`:
```python
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
```
- UI Framework: Streamlit (`st.selectbox`, `st.button`, `st.beta_columns`).
- Artifacts loaded: `model/movie_list.pkl` (Pandas DataFrame) and `model/similarity.pkl` (dense matrix).

---

## 7. Shortcomings and Required Modernizations

While the reference methodology is clear and effective for teaching, several implementation aspects require engineering modernization:

| Area | Reference Implementation | Modernized CineMatch Implementation |
|---|---|---|
| **API Security** | Hardcoded TMDB API key in public code | Environment variable `TMDB_API_KEY`, `.env.example`, zero credentials in Git |
| **Poster Robustness** | Crashes on missing `poster_path` or failed HTTP response | Status check, 3-second timeout, local cached responses, graceful SVG/PNG fallback |
| **Merge Safety** | Merges on `title` (prone to duplicate title ambiguity) | Merges on `id == movie_id` or verifies title parity |
| **JSON Parsing Safety** | Unhandled `ast.literal_eval` exceptions on malformed strings | Robust `try-except` parsing with schema validation |
| **Storage / Memory** | Uncompressed $185\text{ MB}$ dense float64 matrix pickle | Compressed top-K precomputed matrix or sparse cosine computation ($<15\text{ MB}$) |
| **Streamlit API** | Deprecated `st.beta_columns(5)` | Modern `st.columns(5)`, responsive CSS layout |
| **Error Handling** | Unhandled `IndexError` on unknown movie titles | Safe search, case-insensitive fuzzy lookup, user-friendly UI warnings |
| **Reproducibility** | Ad-hoc Kaggle notebook cells | Modular CLI pipeline (`python -m src.train`), automated tests (`pytest`), typed modules |
| **Evaluation** | No quantitative evaluation or diagnostics | Coverage, self-exclusion verification, rank consistency, genre overlap diagnostics |
