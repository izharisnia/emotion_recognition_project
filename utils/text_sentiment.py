import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

_sia = None

def _ensure():
    global _sia
    try:
        if _sia is None:
            try:
                _ = nltk.data.find("sentiment/vader_lexicon.zip")
            except LookupError:
                nltk.download("vader_lexicon")
            _sia = SentimentIntensityAnalyzer()
    except Exception:
        _sia = None

def vader_polarity(text: str) -> float:
    _ensure()
    if _sia is None:
        return 0.0
    return float(_sia.polarity_scores(text)["compound"])
