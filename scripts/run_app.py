"""Script to launch CineMatch application server with hot-reload."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

import uvicorn

if __name__ == "__main__":
    print("=" * 65)
    print("Starting CineMatch Application Server...")
    print("Access Web UI at:  http://localhost:8000")
    print("API Documentation: http://localhost:8000/api/docs")
    print("=" * 65)
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=False)
