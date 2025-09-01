from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from database.db_helper import get_db, query_one, query_all, execute
from services.recipe_suggester import RecipeSuggester
from services.feedback_manager import FeedbackManager
from services.auth_service import AuthService
from models.emotion_detector import EmotionDetector
import os
import json

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object("config.Config")
app.secret_key = app.config["SECRET_KEY"]

# Register custom Jinja2 filter to handle JSON strings in templates
app.jinja_env.filters['fromjson'] = json.loads

# Ensure DB file/dir exists at startup
with app.app_context():
    os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)
    get_db()

# Services
recipe_suggester = RecipeSuggester(app.config["DATABASE_PATH"])
feedback_mgr = FeedbackManager(app.config["DATABASE_PATH"])
auth = AuthService(app.config["DATABASE_PATH"])
emo = EmotionDetector(model_path="models/emotion_model.pkl")  # loads if available

# ---------------- Public pages ----------------
@app.get("/")
def home():
    user = auth.current_user()
    return render_template("home.html", user=user, config=app.config)

@app.post("/analyze")
def analyze():
    """
    Accepts JSON { transcript: "...", audio_seconds: float? }
    Returns { mood, confidence, recipe }
    """
    data = request.get_json(silent=True) or {}
    transcript = (data.get("transcript") or "").strip()
    if not transcript:
        return jsonify({"ok": False, "error": "Empty transcript"}), 400

    mood, conf = emo.detect(transcript)
    recipe = recipe_suggester.pick_for_mood(mood)

    # Generate a dynamic image URL
    if recipe:
        recipe_title_sanitized = recipe["title"].replace(" ", "+")
        recipe["image_url"] = f"https://placehold.co/400x300/f97316/fff?text={recipe_title_sanitized}"

    # Save history if logged in
    uid = session.get("uid")
    if uid and recipe:
        execute("""
            INSERT INTO history(user_id, mood, transcript, recipe_id)
            VALUES (?, ?, ?, ?)
        """, (uid, mood, transcript, recipe["id"]))

    return jsonify({"ok": True, "mood": mood, "confidence": round(conf, 3), "recipe": recipe})

@app.get("/recipe/<int:rid>")
def recipe_view(rid: int):
    recipe = query_one("SELECT * FROM recipes WHERE id = ?", (rid,))
    if not recipe:
        flash("Recipe not found", "error")
        return redirect(url_for("home"))
    
    # Convert read-only sqlite3.Row to a mutable dictionary
    recipe = dict(recipe)
    recipe["ingredients"] = json.loads(recipe["ingredients"])
    recipe["steps"] = json.loads(recipe["steps"])

    # Generate a dynamic image URL for the recipe details page
    recipe_title_sanitized = recipe["title"].replace(" ", "+")
    recipe["image_url"] = f"https://placehold.co/600x450/f97316/fff?text={recipe_title_sanitized}"

    return render_template("mood_based_recipe_card.html", recipe=recipe, mood=request.args.get("mood", ""), config=app.config)

# ---------------- Feedback ----------------
@app.post("/feedback")
def feedback():
    data = request.get_json(silent=True) or {}
    rid = data.get("recipe_id")
    mood = data.get("mood")
    val = 1 if data.get("thumb") == "up" else -1
    uid = session.get("uid")
    feedback_mgr.record(uid, rid, mood, val)
    return jsonify({"ok": True})

# ---------------- Auth ----------------
@app.get("/login")
def login_page():
    return render_template("login.html")

@app.post("/login")
def login_post():
    email = request.form.get("email", "").strip().lower()
    pwd = request.form.get("password", "")
    user = auth.login(email, pwd)
    if user:
        session["uid"] = user["id"]
        session["name"] = user["name"]
        # Add the user's email to the session to enable the admin check
        session["email"] = user["email"]
        return redirect(url_for("dashboard"))
    flash("Invalid credentials", "error")
    return redirect(url_for("login_page"))

@app.get("/register")
def register_page():
    return render_template("register.html")

@app.post("/register")
def register_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    pwd = request.form.get("password", "")
    ok, msg = auth.register(name, email, pwd)
    if ok:
        flash("Account created. Please login.", "success")
        return redirect(url_for("login_page"))
    flash(msg or "Registration failed", "error")
    return redirect(url_for("register_page"))

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- User & Admin ----------------
@app.get("/dashboard")
def dashboard():
    uid = session.get("uid")
    if not uid:
        return redirect(url_for("login_page"))
    history = query_all("""
        SELECT h.id, h.mood, h.created_at, r.title as recipe_title, r.id as recipe_id
        FROM history h LEFT JOIN recipes r ON r.id = h.recipe_id
        WHERE h.user_id = ? ORDER BY h.created_at DESC
    """, (uid,))
    return render_template("dashboard.html", history=history)

@app.get("/admin")
def admin():
    stats = {
        "users": query_one("SELECT COUNT(*) c FROM users")["c"],
        "recipes": query_one("SELECT COUNT(*) c FROM recipes")["c"],
        "history": query_one("SELECT COUNT(*) c FROM history")["c"],
        "thumbs_up": query_one("SELECT COUNT(*) c FROM feedback WHERE value = 1")["c"],
        "thumbs_down": query_one("SELECT COUNT(*) c FROM feedback WHERE value = -1")["c"],
        "top_moods": query_all("SELECT mood, COUNT(*) c FROM history GROUP BY mood ORDER BY c DESC LIMIT 5")
    }
    return render_template("admin_dashboard.html", stats=stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"], debug=True)
