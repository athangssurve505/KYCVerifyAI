import numpy as np
import tensorflow as tf
import cv2
import sys
from pathlib import Path

from feature_extraction import process_video_to_features

# -------------------------------
# CONFIG
# -------------------------------
MODEL_PATH = "data/models/best_model.h5"
TARGET_FRAMES = 90
THRESHOLD = 0.5

# -------------------------------
# Load model
# -------------------------------
print("Loading trained model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("Model loaded!")

# -------------------------------
# Predict function
# -------------------------------
def predict_video(video_path: str):
    print(f"\nProcessing video: {video_path}")

    features = process_video_to_features(
        video_path,
        target_frames=TARGET_FRAMES,
        extract_temporal=True
    )

    if features is None:
        print("❌ Failed to extract features")
        return

    # Model expects batch dimension
    X = np.expand_dims(features, axis=0)

    prob = model.predict(X)[0][0]
    label = "REAL" if prob >= THRESHOLD else "FAKE"
    confidence = prob if label == "REAL" else 1 - prob

    print("\n=== DEEPFAKE DETECTION RESULT ===")
    print(f"Prediction : {label}")
    print(f"Confidence : {confidence * 100:.2f}%")
    print("================================")

    return label, confidence

# -------------------------------
# CLI entry
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_deepfake.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    predict_video(video_path)
