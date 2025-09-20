# recommender.py
from pathlib import Path
import pandas as pd
from typing import List

def _load_content() -> pd.DataFrame:
    """Try multiple file locations; if not found, return a small built-in sample dataframe."""
    possible = [
        Path("data/content.csv"),
        Path("content.csv"),
        Path("./data/content.csv"),
        Path("./content.csv")
    ]
    for p in possible:
        if p.exists():
            try:
                df = pd.read_csv(p)
                # Normalize columns (safe defaults)
                df.columns = [c.strip() for c in df.columns]
                # Ensure important columns exist
                for col in ("content_id", "title", "subject", "difficulty", "type"):
                    if col not in df.columns:
                        raise ValueError(f"Missing column '{col}' in {p}")
                # Normalize text fields
                df["subject"] = df["subject"].astype(str).str.title().str.strip()
                df["difficulty"] = df["difficulty"].astype(str).str.title().str.strip()
                return df
            except Exception as e:
                # If reading failed, continue to fallback
                print(f"Error reading {p}: {e}")
                continue

    # Fallback sample dataset
    sample = [
        {"content_id": 1, "title": "Algebra Basics", "subject": "Math", "difficulty": "Easy", "type": "Video"},
        {"content_id": 2, "title": "Advanced Geometry", "subject": "Math", "difficulty": "Hard", "type": "Quiz"},
        {"content_id": 3, "title": "Human Body Systems", "subject": "Science", "difficulty": "Medium", "type": "Text"},
        {"content_id": 4, "title": "World War II Overview", "subject": "History", "difficulty": "Medium", "type": "Video"},
        {"content_id": 5, "title": "Photosynthesis Basics", "subject": "Science", "difficulty": "Easy", "type": "Quiz"},
        {"content_id": 6, "title": "Linear Equations", "subject": "Math", "difficulty": "Medium", "type": "Text"},
        {"content_id": 7, "title": "Cell Structure", "subject": "Science", "difficulty": "Easy", "type": "Video"},
        {"content_id": 8, "title": "Indian Independence", "subject": "History", "difficulty": "Hard", "type": "Text"},
        {"content_id": 9, "title": "Probability Intro", "subject": "Math", "difficulty": "Medium", "type": "Video"},
        {"content_id": 10,"title": "Periodic Table", "subject": "Science", "difficulty": "Medium", "type": "Quiz"},
        {"content_id": 11,"title": "Medieval India", "subject": "History", "difficulty": "Easy", "type": "Text"},
        {"content_id": 12,"title": "Quadratic Equations", "subject": "Math", "difficulty": "Hard", "type": "Video"},
        {"content_id": 13,"title": "Ecosystems", "subject": "Science", "difficulty": "Hard", "type": "Text"},
        {"content_id": 14,"title": "Renaissance Art", "subject": "History", "difficulty": "Medium", "type": "Video"},
        {"content_id": 15,"title": "Fractions & Decimals", "subject": "Math", "difficulty": "Easy", "type": "Text"},
        {"content_id": 16,"title": "Genetics Basics", "subject": "Science", "difficulty": "Medium", "type": "Video"},
        {"content_id": 17,"title": "Modern World Conflicts", "subject": "History", "difficulty": "Hard", "type": "Quiz"},
        {"content_id": 18,"title": "Coordinate Geometry", "subject": "Math", "difficulty": "Medium", "type": "Text"},
        {"content_id": 19,"title": "Acids and Bases", "subject": "Science", "difficulty": "Easy", "type": "Quiz"},
        {"content_id": 20,"title": "Constitution of India", "subject": "History", "difficulty": "Medium", "type": "Text"},
    ]
    df = pd.DataFrame(sample)
    return df

# Load once (module-level)
CONTENT_DF = _load_content()

def _score_to_difficulty(score: float) -> str:
    """
    Convert numeric score (0-100) into difficulty bucket.
    <50 -> Easy, 50-75 -> Medium, >75 -> Hard
    """
    try:
        s = float(score)
    except Exception:
        s = 50.0
    if s < 50:
        return "Easy"
    if s <= 75:
        return "Medium"
    return "Hard"

def recommend(interests: List[str], score: float, top_k: int = 10) -> pd.DataFrame:
    """
    Return DataFrame of recommended content.
    - interests: list of subject strings (e.g., ["Math", "Science"])
    - score: last quiz score 0-100
    """
    df = CONTENT_DF.copy()
    # normalize interests
    interests_norm = [str(i).title().strip() for i in (interests or []) if str(i).strip()]
    difficulty = _score_to_difficulty(score)

    # If user provided no interests, return top items of that difficulty across subjects
    if not interests_norm:
        results = df[df["difficulty"] == difficulty].head(top_k)
        return results

    # Filter by interest and difficulty
    results = df[(df["subject"].isin(interests_norm)) & (df["difficulty"] == difficulty)].head(top_k)

    # If no matches found, relax difficulty filter (try nearby difficulties)
    if results.empty:
        # try same subject with any difficulty
        relaxed = df[df["subject"].isin(interests_norm)].head(top_k)
        if not relaxed.empty:
            return relaxed
        # otherwise return top items overall of chosen difficulty
        fallback = df[df["difficulty"] == difficulty].head(top_k)
        return fallback

    return results
