#!/usr/bin/env bash
set -e

# Optional: bootstrap DB
python database/seed_recipes.py

# Ensure VADER lexicon
python - <<'PY'
import nltk
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")
PY

export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
