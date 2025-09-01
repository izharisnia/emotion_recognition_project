#!/usr/bin/env bash
set -euo pipefail

# 1) Seed DB if needed (safe to run multiple times)
python database/seed_recipes.py || true

# 2) Ensure VADER lexicon exists (NLTK)
python - <<'PY'
import nltk
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except Exception:
    nltk.download("vader_lexicon")
PY

# 3) Start Gunicorn (Render provides $PORT env var)
exec gunicorn --workers 4 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT app:app
