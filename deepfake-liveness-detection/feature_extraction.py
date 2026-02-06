"""
Feature Extraction using MediaPipe Face Landmarker (MediaPipe 0.10+)
Extracts 468 3D facial landmarks and temporal dynamics
"""

import cv2
import numpy as np
import mediapipe as mp
import logging
from typing import List, Optional

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
# FACIAL LANDMARK EXTRACTION
# =========================================================

class FacialLandmarkExtractor:
    """
    Extract facial landmarks using MediaPipe Face Landmarker (0.10+ API)
    """

    def __init__(self, max_num_faces: int = 1):
        """
        Initialize MediaPipe Face Landmarker
        """

        base_options = python.BaseOptions(
            model_asset_path="data/models/face_landmarker.task"
        )


        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=max_num_faces,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)
        logger.info("MediaPipe Face Landmarker initialized")

    def extract_landmarks_from_frame(
        self, frame: np.ndarray
    ) -> Optional[np.ndarray]:
        """
        Extract landmarks from a single frame

        Args:
            frame: BGR image (OpenCV)

        Returns:
            (468, 3) landmark array or None
        """

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB, data=rgb_frame
        )

        result = self.detector.detect(mp_image)

        if not result.face_landmarks:
            return None

        landmarks = result.face_landmarks[0]

        return np.array([[lm.x, lm.y, lm.z] for lm in landmarks])

    def extract_landmarks_from_video(
        self, frames: List[np.ndarray], target_frames: int = 90
    ) -> Optional[np.ndarray]:
        """
        Extract landmarks from multiple frames and resample

        Returns:
            (target_frames, 468, 3)
        """

        sequence = []

        for frame in frames:
            lm = self.extract_landmarks_from_frame(frame)
            if lm is not None:
                sequence.append(lm)

        if len(sequence) == 0:
            logger.warning("No face detected in video")
            return None

        sequence = np.array(sequence)

        if len(sequence) != target_frames:
            sequence = self._resample_sequence(sequence, target_frames)

        return sequence

    def _resample_sequence(
        self, sequence: np.ndarray, target_length: int
    ) -> np.ndarray:
        """
        Resample sequence using linear interpolation
        """

        from scipy.interpolate import interp1d

        old_len = len(sequence)
        old_idx = np.linspace(0, old_len - 1, old_len)
        new_idx = np.linspace(0, old_len - 1, target_length)

        resampled = np.zeros(
            (target_length, sequence.shape[1], sequence.shape[2])
        )

        for i in range(sequence.shape[1]):
            for j in range(sequence.shape[2]):
                f = interp1d(old_idx, sequence[:, i, j], kind="linear")
                resampled[:, i, j] = f(new_idx)

        return resampled

    def close(self):
        """Release MediaPipe resources"""
        self.detector.close()


# =========================================================
# TEMPORAL FEATURE EXTRACTION
# =========================================================

class TemporalFeatureExtractor:
    """
    Computes temporal derivatives for LSTM learning
    """

    @staticmethod
    def normalize_landmarks(landmarks: np.ndarray) -> np.ndarray:
        normalized = landmarks.copy()

        for i in range(len(normalized)):
            center = np.mean(normalized[i], axis=0)
            normalized[i] -= center

            scale = np.max(np.linalg.norm(normalized[i], axis=1))
            if scale > 1e-6:
                normalized[i] /= scale

        return normalized

    @staticmethod
    def compute_velocities(landmarks: np.ndarray) -> np.ndarray:
        v = np.zeros_like(landmarks)
        v[1:] = landmarks[1:] - landmarks[:-1]
        return v

    @staticmethod
    def compute_accelerations(velocities: np.ndarray) -> np.ndarray:
        a = np.zeros_like(velocities)
        a[1:] = velocities[1:] - velocities[:-1]
        return a

    @staticmethod
    def compute_jerk(accelerations: np.ndarray) -> np.ndarray:
        j = np.zeros_like(accelerations)
        j[1:] = accelerations[1:] - accelerations[:-1]
        return j

    @staticmethod
    def extract_all_features(landmarks: np.ndarray) -> np.ndarray:
        """
        Returns:
            (frames, 468, 12)
            [x,y,z | vx,vy,vz | ax,ay,az | jx,jy,jz]
        """

        norm = TemporalFeatureExtractor.normalize_landmarks(landmarks)
        vel = TemporalFeatureExtractor.compute_velocities(norm)
        acc = TemporalFeatureExtractor.compute_accelerations(vel)
        jerk = TemporalFeatureExtractor.compute_jerk(acc)

        return np.concatenate([norm, vel, acc, jerk], axis=2)


# =========================================================
# FULL VIDEO → FEATURE PIPELINE
# =========================================================

def process_video_to_features(
    video_path: str,
    target_frames: int = 90,
    extract_temporal: bool = True,
) -> Optional[np.ndarray]:
    """
    Video → frames → landmarks → temporal features
    """

    from utils import VideoProcessor

    frames = VideoProcessor.extract_frames(
        video_path, max_frames=target_frames
    )

    if len(frames) == 0:
        logger.error(f"Frame extraction failed: {video_path}")
        return None

    extractor = FacialLandmarkExtractor()
    landmarks = extractor.extract_landmarks_from_video(
        frames, target_frames
    )
    extractor.close()

    if landmarks is None:
        logger.error(f"Landmark extraction failed: {video_path}")
        return None

    if extract_temporal:
        features = TemporalFeatureExtractor.extract_all_features(landmarks)
    else:
        features = landmarks

    logger.info(f"Features extracted: {features.shape}")
    return features


# =========================================================
# MODULE TEST
# =========================================================

if __name__ == "__main__":
    print("Feature extraction module loaded successfully")
    print("MediaPipe Face Landmarker (0.10+)")
    print("Landmarks: 468")
    print("Temporal features: velocity, acceleration, jerk")
