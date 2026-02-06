"""
Setup script for Deepfake Detection project
Makes the package installable with: pip install -e .
"""
from setuptools import setup, find_packages

setup(
    name="deepfake-detection",
    version="1.0.0",
    description="Temporal Liveness Detection for Deepfake Detection",
    author="Nilesh",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.16.0",
        "keras>=3.0.0",
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "numpy>=1.24.0,<2.0.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.14.0",
        "tqdm>=4.65.0",
        "pillow>=10.0.0",
        "imageio>=2.31.0",
        "imageio-ffmpeg>=0.4.9",
        "kaggle>=1.5.16",
    ],
    python_requires=">=3.8,<3.12",
)