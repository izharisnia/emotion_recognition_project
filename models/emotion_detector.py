"""
Hybrid detector:
- If a trained model file exists (models/emotion_model.pkl), use it on TRANSCRIPTS (text) if features were text-based,
  or use it on AUDIO features if you extend to server-side audio later.
- For this app, we infer emotion from TEXT (browser STT) via rules + VADER; trained model is optional upgrade.
"""
import os
import joblib
from utils.text_sentiment import vader_polarity

KEYWORD_MAP = {
    "stressed": ["stress", "tired", "overwhelmed", "anxious", "pressure", "busy", "tense"],
    "sad": ["sad", "down", "upset", "lonely", "depressed", "cry"],
    "excited": ["excited", "pumped", "thrilled", "hyped", "ecstatic", "surprised"],
    "happy": ["happy", "great", "awesome", "good", "cheerful", "joy"],
    "energized": ["energy", "energetic", "powerful", "strong", "fresh", "neutral", "calm"]
}
MOODS = ["happy", "sad", "stressed", "excited", "energized"]

class EmotionDetector:
    def __init__(self, model_path: str | None = None):
        self.model = None
        self.model_path = model_path
        if model_path and os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception:
                self.model = None

    def _keyword_vote(self, text: str) -> str | None:
        t = text.lower()
        for mood, words in KEYWORD_MAP.items():
            if any(w in t for w in words):
                return mood
        return None

    def detect(self, transcript: str) -> tuple[str, float]:
        # Primary: rules + VADER (fast & robust)
        kw = self._keyword_vote(transcript)
        score = vader_polarity(transcript)  # -1..+1

        if kw:
            if kw in ("sad", "stressed"):
                conf = max(0.7, 0.5 + abs(min(0, score)))
                return kw, conf
            if kw in ("happy", "excited", "energized"):
                conf = max(0.7, 0.5 + max(0, score))
                return kw, conf

        if score >= 0.35:
            return "happy", float(min(1.0, 0.6 + score/2))
        if score <= -0.35:
            tag = "stressed" if "stress" in transcript.lower() else "sad"
            return tag, float(min(1.0, 0.6 + abs(score)/2))
        return "energized", 0.55
