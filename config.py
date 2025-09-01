import os

class Config:
    APP_NAME = "EmoRecipe"
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "emorecipe.sqlite3")
    SECRET_KEY = os.environ.get("EMORECIPE_SECRET", "dev-keep-this-secret")
    PORT = int(os.environ.get("PORT", 5000))
