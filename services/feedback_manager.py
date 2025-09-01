from database.db_helper import execute

class FeedbackManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def record(self, user_id, recipe_id, mood, value: int):
        execute("""
            INSERT INTO feedback(user_id, recipe_id, mood, value)
            VALUES (?, ?, ?, ?)
        """, (user_id, recipe_id, mood, value))
