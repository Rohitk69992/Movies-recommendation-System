# Dataset Documentation: TMDB 5000 Movie Dataset

## 1. Overview & Provenance

The CineMatch recommender system uses the **TMDB 5000 Movie Dataset**, the exact canonical dataset used in the CampusX reference implementation.
- **Original Source**: The Movie Database (TMDB) API via Kaggle (uploaded by user `tmdb` / `sohier`).
- **Acquired Mirror**: Publicly documented GitHub dataset distribution matching the exact Kaggle version.
- **License / Terms of Use**:
  - Creative Commons CC0 / Public Domain for the Kaggle distribution.
  - Film metadata provided courtesy of The Movie Database (TMDB). This product uses the TMDB API and dataset but is not endorsed or certified by TMDB.
- **Download Date**: October 22, 2026.

---

## 2. File Verification & Checksums

| File Name | Path | Byte Size | SHA-256 Checksum |
|---|---|---|---|
| `tmdb_5000_movies.csv` | `data/raw/tmdb_5000_movies.csv` | 5,698,602 bytes | `1e0584a8dd374120e4ed4f2b81f0d2bd0eb95a554708e4a350d00ed5c46d2825` |
| `tmdb_5000_credits.csv` | `data/raw/tmdb_5000_credits.csv` | 40,044,293 bytes | `9d0050599ff88d40366c4841204b1489862bca346bfa46c20b05a65d14508435` |

---

## 3. Schema & Descriptions

### 3.1 `tmdb_5000_movies.csv` (4,803 rows $\times$ 20 columns)
- `id` (int64): Unique TMDB movie identifier.
- `title` (object): Official movie release title.
- `overview` (object): Free-text narrative summary (3 missing values).
- `genres` (object): Serialized JSON array of genre objects `[{"id": 28, "name": "Action"}, ...]`.
- `keywords` (object): Serialized JSON array of topic keywords `[{"id": 1463, "name": "culture clash"}, ...]`.
- `budget` (int64): Production budget in USD.
- `revenue` (int64): Global box office revenue in USD.
- `popularity` (float64): TMDB popularity index score.
- `vote_average` (float64): Mean user rating (0.0 to 10.0 scale).
- `vote_count` (int64): Total number of user ratings recorded.
- `release_date` (object): YYYY-MM-DD release date string (1 missing value).
- `runtime` (float64): Film length in minutes (2 missing values).
- `original_language` (object): ISO-639-1 language code.
- `original_title` (object): Original title before localized release.
- `production_companies` (object): Serialized JSON array of studios.
- `production_countries` (object): Serialized JSON array of production nations.
- `spoken_languages` (object): Serialized JSON array of languages.
- `status` (object): Release status (`Released`, `Post Production`, `Rumored`).
- `tagline` (object): Marketing tagline string (844 missing values).
- `homepage` (object): Official movie website URL (3,091 missing values).

### 3.2 `tmdb_5000_credits.csv` (4,803 rows $\times$ 4 columns)
- `movie_id` (int64): Foreign key matching `id` in `movies.csv`.
- `title` (object): Movie title string.
- `cast` (object): Serialized JSON array of cast members with character names, actor names, and billing order (`order: 0, 1, 2...`).
- `crew` (object): Serialized JSON array of crew members with departments and specific jobs (e.g. `job: 'Director'`).

---

## 4. Key Data Quality Findings

1. **Title Homonyms**:
   Three titles are duplicated across different release years:
   - *The Host* (2006, Bong Joon-ho vs. 2013, Andrew Niccol)
   - *Batman* (1989, Tim Burton vs. 1966, Leslie H. Martinson)
   - *Out of the Blue* (1980, Dennis Hopper vs. 2006, Robert Sarkies)
   *Engineering resolution*: Merge on `id == movie_id` rather than raw `title` to prevent combinatorial cross-joining of unrelated cast/crew.

2. **Null Values in Content Fields**:
   - `overview`: 3 rows missing (`To Be Frank, Sinatra at 100`, `The Mongol King`, `Chiamatemi Francesco - Il Papa della gente`). Treated by imputation of an empty string or removal if metadata is entirely devoid of features.
   - `genres`, `keywords`, `cast`, `crew`: Contain empty arrays `[]` for certain low-budget or obscure titles, handled safely by defaulting to empty lists.

---

## 5. Storage Layout

```text
data/
├── raw/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
├── processed/
│   ├── movies_metadata.parquet
│   └── movies_tags.parquet
└── README.md
```
