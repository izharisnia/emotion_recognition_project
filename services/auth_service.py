from database.db_helper import query_one, execute
from flask import session
import hashlib

def _hash(pw: str) -> str:
    return hashlib.sha256(("emorecipe::" + pw).encode()).hexdigest()

class AuthService:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def register(self, name: str, email: str, password: str):
        if not (name and email and password):
            return False, "All fields required."
        if query_one("SELECT id FROM users WHERE email = ?", (email,)):
            return False, "Email already registered."
        execute("INSERT INTO users(name, email, password_hash) VALUES(?, ?, ?)",
                (name, email, _hash(password)))
        return True, None

    def login(self, email: str, password: str):
        user = query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user and user["password_hash"] == _hash(password):
            return user
        return None

    def current_user(self):
        uid = session.get("uid")
        if not uid:
            return None
        return query_one("SELECT id, name, email FROM users WHERE id = ?", (uid,))
