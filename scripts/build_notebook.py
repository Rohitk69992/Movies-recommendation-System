import json
import io
import contextlib
import os
import pandas as pd
import numpy as np

os.makedirs('notebooks', exist_ok=True)

# Helper to run code and capture stdout
def run_and_capture(code_str, local_vars):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        exec(code_str, local_vars)
    return f.getvalue()

local_env = {}

code_cells = [
    {
        "title": "## 1. Environment & Data Ingestion",
        "code": """import os, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ratings = pd.read_csv('data/raw/ml-latest-small/ratings.csv')
movies = pd.read_csv('data/raw/ml-latest-small/movies.csv')
tags = pd.read_csv('data/raw/ml-latest-small/tags.csv')
links = pd.read_csv('data/raw/ml-latest-small/links.csv')

print(f"Ratings shape: {ratings.shape}")
print(f"Movies shape:  {movies.shape}")
print(f"Tags shape:    {tags.shape}")
print(f"Links shape:   {links.shape}")"""
    },
    {
        "title": "## 2. Integrity, Nulls, and Duplicate Checks",
        "code": """print("Ratings nulls:", ratings.isnull().sum().to_dict())
print("Movies nulls: ", movies.isnull().sum().to_dict())
print("Tags nulls:   ", tags.isnull().sum().to_dict())
print("Links nulls:  ", links.isnull().sum().to_dict())

dup_ratings = ratings.duplicated(subset=['userId', 'movieId']).sum()
dup_movies = movies.duplicated(subset=['movieId']).sum()
print(f"Duplicate user-movie pairs: {dup_ratings}")
print(f"Duplicate movieId records:  {dup_movies}")"""
    },
    {
        "title": "## 3. Matrix Sparsity Analysis",
        "code": """n_users = ratings['userId'].nunique()
n_movies = ratings['movieId'].nunique()
n_ratings = len(ratings)
total_possible = n_users * n_movies
sparsity = (1.0 - (n_ratings / total_possible)) * 100.0

print(f"Unique Users:        {n_users:,}")
print(f"Unique Rated Movies: {n_movies:,}")
print(f"Total Interactions:  {n_ratings:,}")
print(f"Matrix Sparsity:     {sparsity:.4f}%")"""
    },
    {
        "title": "## 4. Rating Distribution Statistics",
        "code": """rating_counts = ratings['rating'].value_counts().sort_index()
print("Rating Value Distribution:")
print(rating_counts)
print(f"Mean Rating:   {ratings['rating'].mean():.3f}")
print(f"Median Rating: {ratings['rating'].median():.3f}")
print(f"Std Dev:       {ratings['rating'].std():.3f}")"""
    },
    {
        "title": "## 5. Activity & Popularity Long Tails",
        "code": """user_act = ratings.groupby('userId').size()
print("User Activity Percentiles:")
print(user_act.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]))

movie_pop = ratings.groupby('movieId').size()
print("\\nMovie Popularity Percentiles:")
print(movie_pop.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]))"""
    },
    {
        "title": "## 6. Genre Diversity & Categorical Profiles",
        "code": """genre_counts = movies['genres'].str.split('|').explode().value_counts()
print("Genre Frequency across 9,742 Catalog Movies:")
print(genre_counts)"""
    },
    {
        "title": "## 7. Temporal Range and Timestamp Validation",
        "code": """ratings['datetime'] = pd.to_datetime(ratings['timestamp'], unit='s')
print(f"First rating timestamp: {ratings['datetime'].min()}")
print(f"Last rating timestamp:  {ratings['datetime'].max()}")
print(f"Temporal span: {(ratings['datetime'].max() - ratings['datetime'].min()).days} days (~22.5 years)")"""
    }
]

notebook_json = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# CineMatch — Exploratory Data Analysis & Data Quality Audit\n",
                "\n",
                "**Author**: Senior ML Engineering & Data Science Team  \n",
                "**Dataset**: GroupLens MovieLens Latest-Small  \n",
                "**Status**: Fully Executed Real Data Pipeline"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.11.9"
        },
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

exec_counter = 1
for item in code_cells:
    # Markdown header cell
    notebook_json["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [item["title"]]
    })
    
    # Run code and capture real output
    raw_output = run_and_capture(item["code"], local_env)
    
    # Code cell
    lines = [l + "\n" for l in item["code"].split("\n")]
    if lines and lines[-1].endswith("\n"):
        lines[-1] = lines[-1][:-1]
        
    out_lines = [l + "\n" for l in raw_output.split("\n")]
    if out_lines and out_lines[-1] == "\n":
        out_lines = out_lines[:-1]

    cell = {
        "cell_type": "code",
        "execution_count": exec_counter,
        "metadata": {},
        "source": lines,
        "outputs": [
            {
                "name": "stdout",
                "output_type": "stream",
                "text": out_lines
            }
        ]
    }
    notebook_json["cells"].append(cell)
    exec_counter += 1

out_path = "notebooks/01_data_quality_and_eda.ipynb"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(notebook_json, f, indent=2)

print(f"Successfully generated executed notebook at {out_path} with {len(notebook_json['cells'])} cells.")
