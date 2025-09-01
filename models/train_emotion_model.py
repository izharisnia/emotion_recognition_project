import os
import glob
import numpy as np
import soundfile as sf
import librosa
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from tqdm import tqdm   # NEW

DATA_DIR = "data/TESS"
MODEL_OUT = "models/emotion_model.pkl"
SR = 22050

def label_from_path(path: str) -> str:
    p = path.lower()
    if "_neutral_" in p:
        return "energized"
    if "_happy_" in p:
        return "happy"
    if "_sad_" in p:
        return "sad"
    if "_ps_" in p or "_pleasant" in p or "_surprise_" in p:
        return "excited"
    if "_angry_" in p or "_anger_" in p or "_disgust_" in p or "_fear_" in p:
        return "stressed"
    return "energized"

def mfcc_features(y: np.ndarray, sr: int) -> np.ndarray:
    y = librosa.util.fix_length(y, size=sr*3) if len(y) < sr*3 else y[:sr*3]  # 3s
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    stats = np.hstack([mfcc.mean(axis=1), mfcc.std(axis=1)])
    return stats.astype(np.float32)

def load_dataset():
    wavs = glob.glob(os.path.join(DATA_DIR, "**", "*.wav"), recursive=True)
    X, y = [], []
    for w in tqdm(wavs, desc="Loading audio files"):   # progress bar
        try:
            sig, sr = sf.read(w, always_2d=False)
            if sig.ndim > 1:
                sig = np.mean(sig, axis=1)
            if sr != SR:
                sig = librosa.resample(sig, orig_sr=sr, target_sr=SR)
                sr = SR
            X.append(mfcc_features(sig, sr))
            y.append(label_from_path(w))
        except Exception as e:
            tqdm.write(f"skip: {w} {e}")  # log skipped file
    return np.stack(X), np.array(y)

if __name__ == "__main__":
    if not os.path.isdir(DATA_DIR):
        raise SystemExit(f"TESS folder not found at {DATA_DIR}")

    X, y = load_dataset()
    print("Dataset:", X.shape, y.shape, "classes:", set(y))

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=200))
    ])
    pipe.fit(X_tr, y_tr)
    y_pr = pipe.predict(X_te)
    print(classification_report(y_te, y_pr))

    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(pipe, MODEL_OUT)
    print("Saved:", MODEL_OUT)
