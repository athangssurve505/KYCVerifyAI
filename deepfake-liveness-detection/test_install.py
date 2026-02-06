"""
Simple Installation Test
Tests basic imports without needing project modules
"""
import sys

def test_core_packages():
    """Test that all core packages are installed"""
    print("=" * 60)
    print("TESTING CORE PACKAGE INSTALLATION")
    print("=" * 60)
    
    packages = {
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'tqdm': 'TQDM',
        'scipy': 'SciPy'
    }
    
    installed = []
    missing = []
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✅ {name:20} - INSTALLED")
            installed.append(name)
        except ImportError:
            print(f"❌ {name:20} - MISSING")
            missing.append(name)
    
    print("\n" + "=" * 60)
    print(f"Summary: {len(installed)}/{len(packages)} packages installed")
    print("=" * 60)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed successfully!")
        return True


def test_versions():
    """Print versions of key packages"""
    print("\n" + "=" * 60)
    print("PACKAGE VERSIONS")
    print("=" * 60)
    
    try:
        import tensorflow as tf
        print(f"TensorFlow: {tf.__version__}")
    except:
        pass
    
    try:
        import keras
        print(f"Keras: {keras.__version__}")
    except:
        pass
    
    try:
        import cv2
        print(f"OpenCV: {cv2.__version__}")
    except:
        pass
    
    try:
        import mediapipe as mp
        print(f"MediaPipe: {mp.__version__}")
    except:
        pass
    
    try:
        import numpy as np
        print(f"NumPy: {np.__version__}")
    except:
        pass


def test_gpu():
    """Test GPU availability"""
    print("\n" + "=" * 60)
    print("GPU SUPPORT")
    print("=" * 60)
    
    try:
        import tensorflow as tf
        
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ Found {len(gpus)} GPU(s):")
            for gpu in gpus:
                print(f"   - {gpu.name}")
        else:
            print("ℹ️  No GPU detected - will use CPU")
            print("   (Training will be slower but still works)")
        
        print(f"\nCUDA Support: {tf.test.is_built_with_cuda()}")
        
    except Exception as e:
        print(f"❌ Error checking GPU: {e}")


def test_webcam():
    """Test webcam availability"""
    print("\n" + "=" * 60)
    print("WEBCAM TEST")
    print("=" * 60)
    
    try:
        import cv2
        
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                h, w = frame.shape[:2]
                print(f"✅ Webcam accessible")
                print(f"   Resolution: {w}x{h}")
            else:
                print("⚠️  Webcam opened but couldn't capture frame")
            cap.release()
        else:
            print("ℹ️  No webcam detected")
            print("   (You can still train models and test with video files)")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def test_mediapipe_functionality():
    print("\n" + "=" * 60)
    print("MEDIAPIPE TASKS FUNCTIONALITY TEST")
    print("=" * 60)

    try:
        import numpy as np
        import mediapipe as mp
        from mediapipe.tasks.python import vision
        from mediapipe.tasks.python import BaseOptions

        options = vision.FaceLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="data/models/face_landmarker.task"
            ),
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1
        )

        landmarker = vision.FaceLandmarker.create_from_options(options)

        dummy = np.zeros((480, 640, 3), dtype=np.uint8)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=dummy)

        result = landmarker.detect(mp_image)

        landmarker.close()

        print("✅ MediaPipe Tasks FaceLandmarker initialized successfully")
        print("   Ready to extract 468 facial landmarks")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "INSTALLATION TEST" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Run tests
    packages_ok = test_core_packages()
    test_versions()
    test_gpu()
    test_webcam()
    test_mediapipe_functionality()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if packages_ok:
        print("\n🎉 Installation successful! You're ready to go!")
        print("\nNext steps:")
        print("1. Run: python test_system.py  (for detailed tests)")
        print("2. Download the dataset from Kaggle")
        print("3. Run: python data_preprocessing.py")
        print("4. Run: python train_complete.py")
    else:
        print("\n⚠️  Please install missing packages first:")
        print("pip install -r requirements.txt")
    
    print("=" * 60)


if __name__ == "__main__":
    main()