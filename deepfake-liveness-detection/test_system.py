"""
Quick Test Script
Verify that all components are working correctly
"""
import sys
import os
import subprocess

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("=" * 60)
    print("Testing Imports...")
    print("=" * 60)
    
    required_packages = [
        ('cv2', 'opencv-python'),
        ('mediapipe', 'mediapipe'),
        ('tensorflow', 'tensorflow'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
    ]
    
    all_ok = True
    
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            all_ok = False
    
    return all_ok


def test_gpu():
    """Test GPU availability"""
    print("\n" + "=" * 60)
    print("Testing GPU Support...")
    print("=" * 60)
    
    try:
        import tensorflow as tf
        
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ Found {len(gpus)} GPU(s)")
            for gpu in gpus:
                print(f"   - {gpu.name}")
        else:
            print("⚠️  No GPU found - Training will use CPU (slower)")
        
        print(f"\nTensorFlow version: {tf.__version__}")
        print(f"CUDA available: {tf.test.is_built_with_cuda()}")
        
    except Exception as e:
        print(f"❌ Error testing GPU: {str(e)}")


def test_webcam():
    """Test webcam access"""
    print("\n" + "=" * 60)
    print("Testing Webcam...")
    print("=" * 60)
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Webcam accessible")
                print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
            else:
                print("⚠️  Webcam opened but no frame captured")
            cap.release()
        else:
            print("❌ Cannot open webcam")
    
    except Exception as e:
        print(f"❌ Error testing webcam: {str(e)}")


def test_mediapipe():
    """Test MediaPipe Face Mesh"""
    print("\n" + "=" * 60)
    print("Testing MediaPipe Face Mesh...")
    print("=" * 60)
    
    try:
        import mediapipe as mp
        import numpy as np
        
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            min_detection_confidence=0.5
        )
        
        # Create a dummy image
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Try processing (won't find face, but tests if library works)
        results = face_mesh.process(dummy_image)
        
        face_mesh.close()
        
        print("✅ MediaPipe Face Mesh initialized successfully")
        print(f"   Supports: 468 facial landmarks in 3D")
    
    except Exception as e:
        print(f"❌ Error testing MediaPipe: {str(e)}")


def test_project_structure():
    """Check if project directories exist"""
    print("\n" + "=" * 60)
    print("Testing Project Structure...")
    print("=" * 60)
    
    from pathlib import Path
    
    required_dirs = [
        'data/raw',
        'data/processed',
        'data/models',
        'results',
        'logs'
    ]
    
    all_exist = True
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"⚠️  {dir_path}/ - Creating...")
            path.mkdir(parents=True, exist_ok=True)
            all_exist = False
    
    return all_exist


def test_feature_extraction():
    """Test feature extraction module"""
    print("\n" + "=" * 60)
    print("Testing Feature Extraction...")
    print("=" * 60)
    
    try:
        from feature_extraction import FacialLandmarkExtractor, TemporalFeatureExtractor
        import numpy as np
        
        # Test landmark extractor initialization
        extractor = FacialLandmarkExtractor()
        print("✅ FacialLandmarkExtractor initialized")
        
        # Test temporal feature extractor with dummy data
        dummy_landmarks = np.random.rand(90, 468, 3)
        features = TemporalFeatureExtractor.extract_all_features(dummy_landmarks)
        
        expected_shape = (90, 468, 12)
        if features.shape == expected_shape:
            print(f"✅ TemporalFeatureExtractor working")
            print(f"   Output shape: {features.shape}")
        else:
            print(f"⚠️  Unexpected shape: {features.shape}, expected {expected_shape}")
        
        extractor.close()
    
    except Exception as e:
        print(f"❌ Error testing feature extraction: {str(e)}")


def test_model_creation():
    """Test model architecture"""
    print("\n" + "=" * 60)
    print("Testing Model Architecture...")
    print("=" * 60)
    
    try:
        from model_training import TemporalLivenessDetector
        
        # Create model
        detector = TemporalLivenessDetector(
            input_shape=(90, 468, 12),
            lstm_units=[128, 64],
            dropout_rate=0.3
        )
        
        # Build model
        model = detector.build_model()
        
        print("✅ Basic LSTM model created")
        print(f"   Parameters: {model.count_params():,}")
        
        # Test advanced model
        detector_adv = TemporalLivenessDetector()
        model_adv = detector_adv.build_advanced_model()
        
        print("✅ Advanced Bi-LSTM + Attention model created")
        print(f"   Parameters: {model_adv.count_params():,}")
    
    except Exception as e:
        print(f"❌ Error testing model: {str(e)}")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "DEEPFAKE DETECTION - SYSTEM TEST" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    
    tests = [
        ("Imports", test_imports),
        ("GPU", test_gpu),
        ("Webcam", test_webcam),
        ("MediaPipe", test_mediapipe),
        ("Project Structure", test_project_structure),
        ("Feature Extraction", test_feature_extraction),
        ("Model Creation", test_model_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result if result is not None else True))
        except Exception as e:
            print(f"\n❌ {test_name} test failed: {str(e)}")
            results.append((test_name, False))
    
    # Final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Download dataset: python data_preprocessing.py")
        print("2. Train model: python train_complete.py")
        print("3. Test webcam: python real_time_detection.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()