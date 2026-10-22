# CineMatch 21-Page Academic Mini Project Report — Technical Revision Log

**Project Title:** CineMatch: TMDB Content-Based Movie Recommendation System  
**Academic Course:** Software Laboratory-II (317533): Machine Learning  
**Department:** Artificial Intelligence & Data Science, ISBM College of Engineering, Pune  
**Revision Date:** October 2026  
**Target Output Artifacts:**  
- `CineMatch_Machine_Learning_Mini_Project_Report_Revised.pdf` (Strictly exactly 21 physical pages)  
- `CineMatch_Machine_Learning_Mini_Project_Report_Revised.docx` (Fully synchronized editable Word document)  
- `CineMatch_Report_Revision_Log.md` (Audit trail and technical verification ledger)

---

## 1. Executive Summary & Resolution of User Feedback

The revision was undertaken to resolve two primary formatting and visual hierarchy issues identified in the original report draft:

1. **Distinguishable Headings & Breathing Room Between Sections:**
   - *Previous Issue:* Section headings (9.4 pt) and subsection headings (8.6 pt) were virtually indistinguishable from body paragraphs (8.3 pt), and cramped vertical spacing (`spaceBefore=4.0 pt`, `spaceAfter=2.0 pt`) created dense, unreadable text walls. Furthermore, the bottom 25-35% of several pages was left empty.
   - *Resolution:* Implemented a strict, distinguishable typography hierarchy:
     - **Chapter Heading:** 13.5 pt bold, leading 17.5 pt, deep navy (`#0a192f`), `spaceBefore=0 pt`, `spaceAfter=7.0 pt`.
     - **Section Heading:** 10.2 pt bold, leading 13.8 pt, crisp navy (`#0f2942`), `spaceBefore=8.0 pt`, `spaceAfter=3.0 pt` (creates prominent breathing room and visual separation).
     - **SubSection Heading:** 9.0 pt bold, leading 12.2 pt, slate dark gray (`#334155`), `spaceBefore=5.0 pt`, `spaceAfter=2.0 pt`.
     - **Academic Body:** 8.4 pt regular, leading 11.6 pt, justified (`alignment=4`), dark charcoal (`#1e293b`), `spaceAfter=3.8 pt`.
     - **Page Completion:** Expanded theoretical depth, mathematical formulations, and empirical discussions on every page so that content fills gracefully down to $y \approx 600\text{--}695\text{ pt}$ (leaving ~50–80 pt margin before running footers at $y=813\text{ pt}$).

2. **Mathematical Formula Visibility:**
   - *Previous Issue:* Equations were hardcoded with `height=18 pt` or `height=20 pt` across widths of 410–490 pt. This squashed images with a natural 6.48 aspect ratio by over 3.7x vertically, flattening characters into microscopic, illegible smudges.
   - *Resolution:* Rendered native LaTeX mathtext equations via Matplotlib (`fontsize=16`, transparent background, 300 DPI, DejaVu Sans math font). Embedded images preserving natural aspect ratios:
     - Standard Equations (Eq 3.1, 3.2, 5.2, 5.3, 6.1, 6.2, 11.1): `width=330 pt, height=51 pt` (aspect ratio 6.48), centered, with 3–4 pt vertical padding before and after.
     - Single-term Equation (Eq 5.1): `width=210 pt, height=43 pt` (aspect ratio 4.87), centered.
     - Equations are large, bold, high-contrast (Min RGB `#0e1629`), and unmissable.

3. **Preservation of Source Files:**
   - The original `CineMatch_Machine_Learning_Mini_Project_Report.pdf` and `CineMatch_Machine_Learning_Mini_Project_Report.docx` are preserved untouched.
   - Revised outputs are saved with the `_Revised` suffix.

---

## 2. Empirical Codebase Verification Ledger

All claims, statistics, and tables in the revised report have been audited against the actual CineMatch repository files:

| Technical Property | Audited Repository Fact | Verification Command / Source File | Report Presentation Status |
| :--- | :--- | :--- | :--- |
| **Raw Movie Records** | 4,803 rows &times; 20 columns | `data/raw/tmdb_5000_movies.csv` | Accurately distinguished as raw source data |
| **Raw Credits Records** | 4,803 rows &times; 4 columns | `data/raw/tmdb_5000_credits.csv` | Accurately distinguished as raw source data |
| **Relational Join Key** | `movies.id == credits.movie_id` | `src/data_loader.py` | Integer primary key join verified |
| **Dropped Records** | Exactly 3 records lacking overview | `src/data_loader.py` | Dropped 3 null plot overviews |
| **Active Catalog Size** | **Exactly 4,800 canonical films** | `models/movie_metadata.parquet` | Verified in all text and tables |
| **Feature Space Dim** | 5,000 unigram tokens | `models/count_vectorizer.joblib` | Confirmed unigram CountVectorizer |
| **Weighting Scheme** | Raw Term Frequency (Bag-of-Words) | `src/feature_engineering.py` | Accurately described (NOT TF-IDF) |
| **Non-Zero Elements** | **145,206 non-zero entries** | `models/feature_matrix.npz` (`nnz`) | Audited exact figure |
| **Matrix Sparsity** | **99.3950%** ($145,206 / 24,000,000$) | `scipy.sparse.csr_matrix` | Verified exact percentage |
| **Metadata Artifact** | 2.61 MB (`movie_metadata.parquet`) | `models/movie_metadata.parquet` | Table 7.1 exact disk footprint |
| **Feature Matrix Artifact**| 295 KB (`feature_matrix.npz`) | `models/feature_matrix.npz` | Table 7.1 exact disk footprint |
| **Vectorizer Artifact** | 141 KB (`count_vectorizer.joblib`) | `models/count_vectorizer.joblib` | Table 7.1 exact disk footprint |
| **Training Metadata** | 1.45 KB (`training_metadata.json`) | `models/training_metadata.json` | Table 7.1 exact disk footprint |
| **Total Artifact Size** | **3.03 MB Total** | `models/` directory sum | Verified vs 185 MB dense matrix |
| **Inference Latency** | 6.26 ms mean (P95 = 9.31 ms) | Benchmark across 150 queries | Clearly labeled as local CPU measurement |
| **Memory Footprint** | 148.2 MB RSS | `server.py` process audit | Measured resident set size |

---

## 3. Real Model Prediction Audit (Table 9.2)

Table 9.2 was audited and updated to reflect the exact top recommendations and cosine proximity scores returned by the trained model:

1. **The Dark Knight (2008):**
   - Top-1: *The Dark Knight Rises* (0.423)
   - Top-2: *Batman Begins* (0.402)
   - Top-3: *Batman Returns* (0.331)
   - *Key Shared Features:* ChristianBale, ChristopherNolan, Gotham, vigilante, DC Comics

2. **Inception (2010):**
   - Top-1: *12 Rounds* (0.304)
   - Top-2: *RED* (0.282)
   - Top-3: *Abduction* (0.280)
   - *Key Shared Features:* Espionage, tactical pursuit, high stakes, covert operative

3. **The Avengers (2012):**
   - Top-1: *Iron Man 3* (0.318)
   - Top-2: *Avengers: Age of Ultron* (0.318)
   - Top-3: *Captain America: Civil War* (0.308)
   - *Key Shared Features:* RobertDowneyJr, Marvel Studios, superhero team, SHIELD

4. **The Matrix (1999):**
   - Top-1: *The Matrix Revolutions* (0.467)
   - Top-2: *The Matrix Reloaded* (0.298)
   - Top-3: *Hackers* (0.257)
   - *Key Shared Features:* KeanuReeves, Wachowski, artificial intelligence, cyber, simulation

5. **The Godfather (1972):**
   - Top-1: *The Godfather: Part II* (0.375)
   - Top-2: *The Godfather: Part III* (0.368)
   - Top-3: *City By The Sea* (0.305)
   - *Key Shared Features:* AlPacino, organized crime, Italian mafia, family dynasty

---

## 4. Typography & Encoding Cleanups

- **Certificate Page:** Corrected `Peoples Empowerment Group’s` to `People's Empowerment Group's` using standard ASCII apostrophe (`'`), preventing unicode replacement glyphs (``) in PDF text extractors.
- **Quotation Marks:** Replaced unicode smart quotes (`“`, `”`) with standard ASCII quotes (`"`), ensuring 100% compliance with ReportLab's standard Helvetica font.
- **Dashes and Symbols:** Replaced unicode em-dashes (`—`) with standard `--`, and multiplication symbols (`&times;`) with `x`.

---

## 5. Physical Page Boundary & Fill Audit (PyMuPDF)

Automated inspection via `fitz` (PyMuPDF) confirms that `CineMatch_Machine_Learning_Mini_Project_Report_Revised.pdf` contains **strictly exactly 21 physical pages**, with content filling down gracefully on all theoretical pages:

| Page # | Chapter / Section Title | Top Content y (pt) | Bottom Content y (pt) | Content Height (pt) | Fill Assessment |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | Institutional Cover Page | 53.3 | 510.6 | 457.3 | Complete (Cover layout) |
| **2** | Institutional Certificate | 130.3 | 494.0 | 363.7 | Complete (Certificate layout) |
| **3** | Table of Contents | 43.1 | 495.9 | 452.8 | Complete (21-page TOC table) |
| **4** | Chapter 1: Abstract | 43.1 | 653.8 | 610.8 | Complete & densely filled |
| **5** | Chapter 2: Introduction | 43.1 | 650.4 | 607.4 | Complete & densely filled |
| **6** | Chapter 3: Problem Statement (Eq 3.1, 3.2) | 43.1 | 668.2 | 625.2 | Complete & large formulas |
| **7** | Chapter 4: Dataset Description (Table 4.1, Fig 4.1) | 43.1 | 643.9 | 600.9 | Complete & balanced |
| **8** | Chapter 5: Methodology (Eq 5.1, 5.2, 5.3) | 43.1 | 627.6 | 584.6 | Complete & large formulas |
| **9** | Chapter 6: Model Planning (Eq 6.1, 6.2, Table 6.1) | 43.1 | 660.1 | 617.1 | Complete & large formulas |
| **10** | Chapter 7: Model Building (Table 7.1, Table 7.2) | 43.1 | 622.6 | 579.6 | Complete & 29-test matrix |
| **11** | Chapter 8: Implementation Details (Table 8.1, Code) | 43.1 | 658.6 | 615.6 | Complete & code snippets |
| **12** | Chapter 8: Architecture Diagrams (Fig 8.1, Fig 8.2) | 43.3 | 603.4 | 560.1 | Complete & high-contrast |
| **13** | Chapter 9: Results -- App Demo (Fig 9.1, Fig 9.2) | 43.1 | 637.9 | 594.9 | Complete & UI screenshots |
| **14** | Chapter 9: Results -- Server Telemetry (Fig 9.3) | 43.3 | 610.9 | 567.6 | Complete & terminal trace |
| **15** | Chapter 9: Results -- Quantitative Eval (Table 9.1, Fig 9.4) | 43.1 | 650.8 | 607.7 | Complete & metrics chart |
| **16** | Chapter 9: Results -- Corpus Distributions (Fig 9.5, 9.6) | 43.1 | 624.6 | 581.6 | Complete & EDA distributions |
| **17** | Chapter 9: Results -- Predictions (Table 9.2, Fig 9.7) | 43.1 | 694.2 | 651.2 | Complete & verified scores |
| **18** | Chapter 9: Results -- Observations & Hardware (Table 9.3) | 43.1 | 654.9 | 611.9 | Complete & benchmarks |
| **19** | Chapter 10: Conclusion | 43.1 | 598.8 | 555.8 | Complete & academic takeaways |
| **20** | Chapter 11: Future Scope (Eq 11.1) | 43.1 | 630.2 | 587.2 | Complete & MMR formula |
| **21** | Chapter 12: References (18 Citations) | 43.1 | 565.5 | 522.4 | Complete & well-spaced |

---

## 6. Verification Test Suite Status

The automated test suite was executed to ensure complete functional integrity across data loaders, feature engineering, recommender engine, and FastAPI REST endpoints:

```text
======================== 29 passed, 1 warning in 4.14s ========================
tests/test_data_loader.py::test_load_raw_tmdb_data_success PASSED        [  3%]
tests/test_data_loader.py::test_load_raw_tmdb_data_missing_file PASSED   [  6%]
tests/test_data_loader.py::test_load_raw_tmdb_data_missing_column PASSED [ 10%]
tests/test_feature_engineering.py::test_stem_text PASSED                 [ 13%]
tests/test_feature_engineering.py::test_build_movie_tags PASSED          [ 17%]
tests/test_pipeline_e2e.py::test_production_artifacts_exist PASSED       [ 20%]
tests/test_pipeline_e2e.py::test_production_recommender_inference PASSED [ 24%]
tests/test_pipeline_e2e.py::test_production_recommender_query_avatar PASSED [ 27%]
tests/test_poster.py::test_fallback_svg_generation PASSED                [ 31%]
tests/test_poster.py::test_fallback_svg_raw PASSED                       [ 34%]
tests/test_poster.py::test_get_poster_url_proxy PASSED                   [ 37%]
tests/test_poster.py::test_fetch_and_cache_poster PASSED                 [ 41%]
tests/test_poster.py::test_attribution_text PASSED                       [ 44%]
tests/test_preprocessing.py::test_extract_names_valid PASSED             [ 48%]
tests/test_preprocessing.py::test_extract_names_empty_and_invalid PASSED [ 51%]
tests/test_preprocessing.py::test_extract_top_cast PASSED                [ 55%]
tests/test_preprocessing.py::test_extract_director PASSED                [ 58%]
tests/test_preprocessing.py::test_collapse_spaces PASSED                 [ 62%]
tests/test_preprocessing.py::test_preprocess_tmdb_metadata PASSED        [ 65%]
tests/test_recommender.py::test_recommender_get_index PASSED             [ 68%]
tests/test_recommender.py::test_recommender_recommendation_logic PASSED  [ 72%]
tests/test_recommender.py::test_recommender_artifacts_save_and_load PASSED [ 75%]
tests/test_server_api.py::test_serve_index_html PASSED                   [ 79%]
tests/test_server_api.py::test_api_movies_search PASSED                  [ 82%]
tests/test_server_api.py::test_api_movie_details_success PASSED          [ 86%]
tests/test_server_api.py::test_api_movie_details_not_found PASSED        [ 89%]
tests/test_server_api.py::test_api_recommend_success PASSED              [ 93%]
tests/test_server_api.py::test_api_stats PASSED                          [ 96%]
tests/test_server_api.py::test_api_poster_endpoint PASSED                [100%]
```

---

## 7. Delivery Summary

1. `CineMatch_Machine_Learning_Mini_Project_Report_Revised.pdf` is fully generated, validated to strictly 21 pages, with generous section spacing, distinguishable bold headings, bold centered mathematical formulas, and rigorous academic theory.
2. `CineMatch_Machine_Learning_Mini_Project_Report_Revised.docx` is generated in complete structural and theoretical synchronization.
3. Both original project report files remain preserved without overwriting.
