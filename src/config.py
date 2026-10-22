"""Global configuration and project paths for CineMatch."""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw" / "ml-latest-small"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
EDA_REPORTS_DIR = REPORTS_DIR / "eda"

# Data File Paths
MOVIES_RAW_PATH = RAW_DATA_DIR / "movies.csv"
RATINGS_RAW_PATH = RAW_DATA_DIR / "ratings.csv"
TAGS_RAW_PATH = RAW_DATA_DIR / "tags.csv"
LINKS_RAW_PATH = RAW_DATA_DIR / "links.csv"

# Preprocessed File Paths
TRAIN_RATINGS_PATH = PROCESSED_DATA_DIR / "train_ratings.csv"
VAL_RATINGS_PATH = PROCESSED_DATA_DIR / "val_ratings.csv"
TEST_RATINGS_PATH = PROCESSED_DATA_DIR / "test_ratings.csv"

# Model Artifact Paths
TFIDF_VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
CONTENT_MATRIX_PATH = MODELS_DIR / "content_matrix.npz"
CONTENT_MAPPINGS_PATH = MODELS_DIR / "content_mappings.joblib"
SVD_MODEL_PATH = MODELS_DIR / "collaborative_svd.joblib"
POPULARITY_STATS_PATH = MODELS_DIR / "popularity_stats.joblib"
HYBRID_CONFIG_PATH = MODELS_DIR / "hybrid_config.json"

# Database Path
SQLITE_DB_PATH = PROJECT_ROOT / "cinematch.db"

# Experiment & Evaluation Configuration
RANDOM_SEED = 42
TEST_SPLIT_RATIO = 0.20  # 20% for test
VAL_SPLIT_RATIO = 0.10   # 10% for validation
TEMPORAL_SPLIT_RATIO = 0.80 # 80% train, 20% test chronologically

# Rating Parameters
MIN_RATING = 0.5
MAX_RATING = 5.0
POSITIVE_RATING_THRESHOLD = 3.5  # Relevance threshold for Precision@K, Recall@K, NDCG@K
BAYESIAN_PRIOR_CONFIDENCE = 10.0 # 'm' parameter for IMDB-style damped ranking

# Content Feature Parameters
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)
GENRE_WEIGHT = 2.0
TAG_WEIGHT = 1.5

# Collaborative SVD Default Hyperparameters
SVD_N_FACTORS = 50
SVD_N_EPOCHS = 25
SVD_LR = 0.005
SVD_REG = 0.05

# Recommendation API Parameters
DEFAULT_TOP_K = 10
MAX_TOP_K = 50
