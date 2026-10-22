"""Initializes CineMatch SQLite database tables and indices safely."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from src.database.db import init_db

if __name__ == "__main__":
    print("Initializing CineMatch SQLite database...")
    init_db()
    print("Database tables initialized successfully!")
