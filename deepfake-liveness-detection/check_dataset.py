"""
Dataset Checker
Verifies that the dataset is downloaded and structured correctly
Compatible with Kaggle DeepFake Videos Dataset
"""

from pathlib import Path


VIDEO_EXTS = ("*.mp4", "*.mov", "*.MOV")


def collect_videos(folder: Path):
    """Collect all video files from a folder using allowed extensions"""
    videos = []
    for ext in VIDEO_EXTS:
        videos.extend(folder.glob(ext))
    return videos


def check_dataset():
    """Check if dataset is ready for preprocessing"""

    print("=" * 60)
    print("DATASET STRUCTURE CHECK")
    print("=" * 60)
    print()

    base_path = Path("data/raw")
    real_path = base_path / "real"
    fake_path = base_path / "fake"
    video_fallback_path = base_path / "video"  # Kaggle real videos

    issues = []

    # ---- Base directory ----
    if not base_path.exists():
        print(f"❌ Directory not found: {base_path}")
        print("   Create it with: mkdir data\\raw")
        issues.append("base_path")
        return False
    else:
        print(f"✅ Found: {base_path}")

    # ---- Fake directory ----
    if not fake_path.exists():
        print(f"❌ Directory not found: {fake_path}")
        print("   Create it with: mkdir data\\raw\\fake")
        issues.append("fake_path")
    else:
        print(f"✅ Found: {fake_path}")

    # ---- Real directory OR fallback ----
    if real_path.exists():
        real_source = real_path
        print(f"✅ Found: {real_path}")
    elif video_fallback_path.exists():
        real_source = video_fallback_path
        print(f"⚠️  'real/' not found, using fallback: {video_fallback_path}")
    else:
        print("❌ No real video directory found")
        print("   Expected one of:")
        print("   - data/raw/real/")
        print("   - data/raw/video/")
        issues.append("real_path")
        real_source = None

    print()

    # ---- Count real videos ----
    if real_source:
        real_videos = collect_videos(real_source)
        print(f"Real videos: {len(real_videos)}")
        if len(real_videos) == 0:
            print("   ⚠️  No real videos found")
            issues.append("no_real_videos")
        else:
            print(f"   ✅ Found {len(real_videos)} real videos")
            for v in real_videos[:3]:
                print(f"      - {v.name}")
            if len(real_videos) > 3:
                print(f"      ... and {len(real_videos) - 3} more")

    print()

    # ---- Count fake videos ----
    if fake_path.exists():
        fake_videos = collect_videos(fake_path)
        print(f"Fake videos: {len(fake_videos)}")
        if len(fake_videos) == 0:
            print("   ⚠️  No fake videos found")
            issues.append("no_fake_videos")
        else:
            print(f"   ✅ Found {len(fake_videos)} fake videos")
            for v in fake_videos[:3]:
                print(f"      - {v.name}")
            if len(fake_videos) > 3:
                print(f"      ... and {len(fake_videos) - 3} more")

    print()

    # ---- CSV metadata (optional) ----
    csv_file = base_path / "DeepFake Videos Dataset.csv"
    if csv_file.exists():
        print(f"✅ Metadata CSV found: {csv_file.name}")
    else:
        print("⚠️  Metadata CSV not found (optional)")

    print()
    print("=" * 60)

    # ---- Summary ----
    if not issues:
        print("✅ DATASET READY!")
        print()
        print("Next step:")
        print("  python data_preprocessing.py")
        print()
        return True
    else:
        print("❌ DATASET NOT READY")
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        return False


def check_processed_data():
    """Check if preprocessed data exists"""

    print()
    print("=" * 60)
    print("PREPROCESSED DATA CHECK")
    print("=" * 60)
    print()

    processed_path = Path("data/processed")
    train_path = processed_path / "train"
    val_path = processed_path / "val"
    test_path = processed_path / "test"

    if not processed_path.exists():
        print("❌ No preprocessed data found")
        print("   Run: python data_preprocessing.py")
        return False

    splits = {"train": train_path, "val": val_path, "test": test_path}
    all_exist = True

    for name, path in splits.items():
        if path.exists():
            samples = list(path.glob("*.npz"))
            print(f"✅ {name:6} - {len(samples)} samples")
        else:
            print(f"❌ {name:6} - not found")
            all_exist = False

    print()

    if all_exist:
        print("✅ PREPROCESSED DATA READY!")
        print("Next step: python train_complete.py")
    else:
        print("❌ PREPROCESSED DATA NOT READY")
        print("Run: python data_preprocessing.py")

    return all_exist


def check_model():
    """Check if trained model exists"""

    print()
    print("=" * 60)
    print("TRAINED MODEL CHECK")
    print("=" * 60)
    print()

    model_path = Path("data/models/best_model.h5")

    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model found: {model_path}")
        print(f"   Size: {size_mb:.2f} MB")
        print("Next step: python real_time_detection.py")
        return True
    else:
        print(f"❌ Model not found: {model_path}")
        print("Train the model first: python train_complete.py")
        return False


def main():
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 18 + "DATASET CHECKER" + " " * 25 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    dataset_ready = check_dataset()
    processed_ready = check_processed_data()
    model_ready = check_model()

    print()
    print("=" * 60)
    print("OVERALL STATUS")
    print("=" * 60)
    print()

    print(f"{'✅' if dataset_ready else '❌'} Raw dataset")
    print(f"{'✅' if processed_ready else '❌'} Preprocessed data")
    print(f"{'✅' if model_ready else '❌'} Trained model")

    print()
    if model_ready:
        print("🎉 Everything ready! You can run real-time detection!")
    elif processed_ready:
        print("📊 Ready to train! Run: python train_complete.py")
    elif dataset_ready:
        print("🔄 Ready to preprocess! Run: python data_preprocessing.py")
    else:
        print("📥 Dataset setup incomplete")


if __name__ == "__main__":
    main()
