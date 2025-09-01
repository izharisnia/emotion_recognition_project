from database.db_helper import query_all
import random

MOOD_BUCKET_MAP = {
    "happy": "celebration",
    "sad": "chocolate",
    "stressed": "comfort",
    "excited": "high_protein",
    "energized": "fresh"
}

class RecipeSuggester:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def pick_for_mood(self, mood: str) -> dict | None:
        bucket = MOOD_BUCKET_MAP.get(mood, "fresh")
        rows = query_all(
            "SELECT * FROM recipes WHERE mood_tag = ? ORDER BY rating DESC, id DESC",
            (bucket,)
        )
        if not rows:
            rows = query_all("SELECT * FROM recipes ORDER BY rating DESC")
        return dict(random.choice(rows)) if rows else None
