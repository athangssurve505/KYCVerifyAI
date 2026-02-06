"""
Real-Time Webcam Liveness Detection
Captures live video, extracts features, and detects deepfakes in real-time
"""
import cv2
import numpy as np
import tensorflow as tf
import keras
from collections import deque
import time
import logging
from pathlib import Path

from feature_extraction import FacialLandmarkExtractor, TemporalFeatureExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealTimeLivenessDetector:
    """Real-time deepfake detection using webcam"""
    
    def __init__(self, 
                 model_path: str,
                 target_frames: int = 90,
                 confidence_threshold: float = 0.5,
                 buffer_size: int = 90):
        """
        Initialize real-time detector
        
        Args:
            model_path: Path to trained model
            target_frames: Number of frames to analyze
            confidence_threshold: Threshold for classification (0-1)
            buffer_size: Size of frame buffer
        """
        self.model_path = model_path
        self.target_frames = target_frames
        self.confidence_threshold = confidence_threshold
        self.buffer_size = buffer_size
        
        # Load model
        logger.info(f"Loading model from {model_path}")
        self.model = keras.models.load_model(model_path)
        logger.info("Model loaded successfully!")
        
        # Initialize landmark extractor
        self.landmark_extractor = FacialLandmarkExtractor(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Frame buffer for temporal analysis
        self.landmark_buffer = deque(maxlen=buffer_size)
        
        # Statistics
        self.fps = 0
        self.processing_time = 0
        self.prediction_result = None
        self.prediction_confidence = 0.0
        
        logger.info("Real-time detector initialized!")
    
    def process_frame(self, frame: np.ndarray) -> dict:
        """
        Process a single frame and update buffer
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            Dictionary with detection results
        """
        start_time = time.time()
        
        # Extract landmarks from frame
        landmarks = self.landmark_extractor.extract_landmarks_from_frame(frame)
        
        if landmarks is None:
            return {
                'face_detected': False,
                'prediction': None,
                'confidence': 0.0,
                'status': 'No face detected'
            }
        
        # Add to buffer
        self.landmark_buffer.append(landmarks)
        
        # Check if we have enough frames for prediction
        if len(self.landmark_buffer) < self.target_frames:
            progress = len(self.landmark_buffer) / self.target_frames * 100
            return {
                'face_detected': True,
                'prediction': None,
                'confidence': 0.0,
                'status': f'Collecting frames... {progress:.0f}%'
            }
        
        # Get last N frames
        recent_landmarks = np.array(list(self.landmark_buffer)[-self.target_frames:])
        
        # Extract temporal features
        features = TemporalFeatureExtractor.extract_all_features(recent_landmarks)
        
        # Reshape for model input: (1, frames, landmarks, features)
        features_input = np.expand_dims(features, axis=0)
        
        # Make prediction
        prediction = self.model.predict(features_input, verbose=0)[0][0]
        
        # Classify
        is_real = prediction >= self.confidence_threshold
        confidence = prediction if is_real else (1 - prediction)
        
        self.processing_time = time.time() - start_time
        
        return {
            'face_detected': True,
            'prediction': 'REAL' if is_real else 'FAKE',
            'confidence': float(confidence),
            'raw_score': float(prediction),
            'status': 'Analysis complete',
            'processing_time': self.processing_time
        }
    
    def draw_results(self, frame: np.ndarray, results: dict) -> np.ndarray:
        """
        Draw detection results on frame
        
        Args:
            frame: Input frame
            results: Detection results dictionary
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        h, w = frame.shape[:2]
        
        # Draw semi-transparent overlay at top
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, annotated, 0.3, 0, annotated)
        
        # Status text
        status = results.get('status', 'Initializing...')
        cv2.putText(annotated, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # If prediction available
        if results.get('prediction'):
            prediction = results['prediction']
            confidence = results['confidence']
            
            # Color based on prediction
            if prediction == 'REAL':
                color = (0, 255, 0)  # Green
                text = f"REAL PERSON"
            else:
                color = (0, 0, 255)  # Red
                text = f"DEEPFAKE DETECTED"
            
            # Draw prediction
            cv2.putText(annotated, text, (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            
            # Draw confidence
            conf_text = f"Confidence: {confidence*100:.1f}%"
            cv2.putText(annotated, conf_text, (10, 105), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # FPS counter
        if self.fps > 0:
            cv2.putText(annotated, f"FPS: {self.fps:.1f}", (w - 150, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Instructions
        cv2.putText(annotated, "Press 'Q' to quit | 'R' to reset", (10, h - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return annotated
    
    def run(self, camera_index: int = 0, window_name: str = "Liveness Detection"):
        """
        Run real-time detection
        
        Args:
            camera_index: Index of camera to use
            window_name: Name of display window
        """
        logger.info(f"Starting webcam capture from camera {camera_index}")
        
        # Open webcam
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            logger.error("Failed to open camera!")
            return
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        logger.info("Press 'Q' to quit, 'R' to reset buffer")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    logger.error("Failed to read frame!")
                    break
                
                # Process frame
                results = self.process_frame(frame)
                
                # Draw results
                annotated_frame = self.draw_results(frame, results)
                
                # Calculate FPS
                frame_count += 1
                elapsed = time.time() - start_time
                if elapsed > 1.0:
                    self.fps = frame_count / elapsed
                    frame_count = 0
                    start_time = time.time()
                
                # Display
                cv2.imshow(window_name, annotated_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    logger.info("Quit signal received")
                    break
                elif key == ord('r') or key == ord('R'):
                    logger.info("Resetting buffer")
                    self.landmark_buffer.clear()
                elif key == ord('s') or key == ord('S'):
                    # Save screenshot
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"detection_{timestamp}.jpg"
                    cv2.imwrite(filename, annotated_frame)
                    logger.info(f"Screenshot saved: {filename}")
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            cv2.destroyAllWindows()
            self.landmark_extractor.close()
            logger.info("Webcam released, windows closed")
    
    def analyze_video_file(self, video_path: str, output_path: str = None):
        """
        Analyze a video file (for testing with pre-recorded videos)
        
        Args:
            video_path: Path to video file
            output_path: Optional path to save annotated video
        """
        logger.info(f"Analyzing video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video: {video_path}")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Video writer for output
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        logger.info(f"Video info - FPS: {fps}, Size: {width}x{height}, Frames: {total_frames}")
        
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            # Process frame
            results = self.process_frame(frame)
            
            # Draw results
            annotated_frame = self.draw_results(frame, results)
            
            # Save to output video
            if output_path:
                out.write(annotated_frame)
            
            # Display
            cv2.imshow('Video Analysis', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            frame_idx += 1
            if frame_idx % 30 == 0:
                logger.info(f"Processed {frame_idx}/{total_frames} frames")
        
        # Cleanup
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
        
        logger.info(f"Video analysis complete!")


def main():
    """Main function for real-time detection"""
    
    print("=" * 60)
    print("REAL-TIME LIVENESS DETECTION")
    print("=" * 60)
    
    # Configuration
    MODEL_PATH = "./data/models/best_model.h5"
    
    # Check if model exists
    if not Path(MODEL_PATH).exists():
        print(f"\n❌ Model not found at {MODEL_PATH}")
        print("Please train the model first using model_training.py")
        return
    
    # Create detector
    detector = RealTimeLivenessDetector(
        model_path=MODEL_PATH,
        target_frames=90,
        confidence_threshold=0.5
    )
    
    print("\n✅ Detector initialized!")
    print("\nControls:")
    print("  Q - Quit")
    print("  R - Reset frame buffer")
    print("  S - Save screenshot")
    
    # Run detection
    detector.run(camera_index=0)


if __name__ == "__main__":
    main()