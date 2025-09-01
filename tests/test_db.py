from app import app
from database.db_helper import query_one

def test_db_seeded():
    with app.app_context():
        row = query_one("SELECT COUNT(*) c FROM recipes")
        assert row["c"] >= 1

