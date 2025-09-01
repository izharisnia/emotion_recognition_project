from models.emotion_detector import EmotionDetector

def test_emotions_rules():
    emo = EmotionDetector()
    m1, _ = emo.detect("I am so stressed and overwhelmed today")
    assert m1 in ("stressed", "sad")
    m2, _ = emo.detect("I feel excited and happy!")
    assert m2 in ("happy", "excited", "energized")
