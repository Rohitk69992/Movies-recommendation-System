# CineMatch — Environment & Workspace Audit

**Date of Audit**: October 22, 2026  
**Auditor**: Senior Data Scientist, ML Engineer, and QA Lead  
**Project**: CineMatch — TMDB Content-Based Movie Recommendation System  

---

## 1. Operating System & Hardware Specifications

- **Operating System**: Microsoft Windows 11 (x86_64 architecture)
- **Shell**: PowerShell
- **Available Storage**: > 200 GB Free on Drive C:
- **Local Working Directory**: `C:\Users\rohit\OneDrive\Desktop\MiniProject`
- **Application Data Directory**: `C:\Users\rohit\.gemini\antigravity`

---

## 2. Python Runtime & Environment Details

- **Python Version**: `3.11.9` (64-bit)
- **Scientific & ML Libraries**:
  - `numpy`: `2.4.4`
  - `pandas`: `2.3.3`
  - `scipy`: `1.17.1`
  - `scikit-learn`: `1.8.0`
  - `nltk`: `3.10.4` (Installed and validated)
  - `joblib`: `1.5.3`
  - `matplotlib`: `3.10.x`
  - `seaborn`: `0.13.2`
  - `streamlit`: `1.59.2`
  - `requests`: `2.34.2`
  - `pytest`: `9.1.1`
  - `python-dotenv`: `1.2.2`

---

## 3. Network & External Services

- **Internet Access**: Verified active.
- **TMDB 5000 Source Repository**: Raw CSVs accessible via GitHub and HuggingFace mirrors.
- **TMDB Poster API**: `https://api.themoviedb.org/3/movie/{id}` (supported with optional `TMDB_API_KEY` and graceful offline fallback).

---

## 4. Storage & Memory Budget Estimation

- **Raw Datasets**:
  - `tmdb_5000_movies.csv`: ~5.7 MB
  - `tmdb_5000_credits.csv`: ~40 MB
  - Combined uncompressed disk footprint: ~45.7 MB
- **In-Memory DataFrame**:
  - Merged raw dataframe: ~4,809 rows $\times$ 23 columns ($\approx 35\text{ MB}$)
  - Processed metadata dataframe: ~4,806 rows $\times$ 7 columns ($\approx 4\text{ MB}$)
- **Vectorization & Similarity**:
  - Bag-of-Words sparse matrix (`scipy.sparse.csr_matrix`): $4806 \times 5000$ $\approx 0.5\text{ MB}$
  - Cosine similarity matrix:
    - Dense float64: $4806 \times 4806 \times 8 \text{ bytes} \approx 184.8\text{ MB}$
    - Dense float32: $\approx 92.4\text{ MB}$
    - Top-$K$ precomputed index (e.g. top 50 neighbours per item): $4806 \times 50 \times 4 \text{ bytes} \approx 0.96\text{ MB}$
    - Sparse/on-the-fly cosine calculation: zero extra disk storage, $< 5\text{ ms}$ query time.
- **Decision**: CineMatch supports both precomputed top-similarity indices/matrices and on-the-fly sparse cosine computations, keeping total artifact disk size $< 15\text{ MB}$ and load time $< 1\text{ second}$.

---

## 5. Implementation Checklist

- [x] **Phase 1**: Reference Repository Inspection & Methodology Documentation (`docs/reference_methodology.md`)
- [x] **Phase 2**: Workspace Audit & Environment Verification (`docs/environment_audit.md`)
- [ ] **Phase 3**: Acquire & Verify TMDB 5000 Dataset (`data/raw/`, `data/README.md`)
- [ ] **Phase 4**: Exploratory Data Analysis (`notebooks/01_eda.ipynb`, `reports/eda/`, `docs/eda_findings.md`)
- [ ] **Phase 5**: Feature Engineering Faithful to Reference (`notebooks/02_feature_engineering.ipynb`, `src/preprocessing.py`, `src/feature_engineering.py`)
- [ ] **Phase 6**: Vectorization & Cosine Similarity Engine (`src/recommender.py`)
- [ ] **Phase 7**: Reusable Artifact Training Pipeline (`src/train.py`, `models/`)
- [ ] **Phase 8**: TMDB Posters & Security Service (`src/poster.py`, `.env.example`)
- [ ] **Phase 9**: Streamlit Application (`app.py`)
- [ ] **Phase 10**: Clean Architecture Alignment
- [ ] **Phase 11**: Scientific Evaluation & Limitations (`src/evaluation.py`, `docs/evaluation.md`)
- [ ] **Phase 12**: Automated Test Suite (`tests/`)
- [ ] **Phase 13**: Clean Project Structure
- [ ] **Phase 14**: College Mini-Project Report (`reports/final_project_report.md`, `docs/viva_questions.md`)
- [ ] **Phase 15**: Reproducibility & End-to-End Validation
- [ ] **Phase 16**: Final Delivery Report
