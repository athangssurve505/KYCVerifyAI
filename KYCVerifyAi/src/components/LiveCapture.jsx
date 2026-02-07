import { useState, useRef, useEffect } from 'react';
import { Camera, Circle, CheckCircle, AlertCircle, X, Upload } from 'lucide-react';
import './LiveCapture.css';

const LiveCapture = () => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [faceDetected, setFaceDetected] = useState(false);
  const [qualityScore, setQualityScore] = useState(0);
  const [captureMode, setCaptureMode] = useState('guided'); // 'guided' or 'manual'
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (isCapturing) {
      startCamera();
      simulateFaceDetection();
    } else {
      stopCamera();
    }

    return () => stopCamera();
  }, [isCapturing]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error('Camera access denied:', err);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const simulateFaceDetection = () => {
    // Simulate face detection (replace with actual ML model)
    const interval = setInterval(() => {
      const detected = Math.random() > 0.3;
      setFaceDetected(detected);
      if (detected) {
        setQualityScore(Math.floor(Math.random() * 30) + 70);
      } else {
        setQualityScore(0);
      }
    }, 500);

    return () => clearInterval(interval);
  };

  const captureFrame = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (canvas && video) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      const imageData = canvas.toDataURL('image/jpeg');
      setCapturedImage(imageData);
      setIsCapturing(false);
      
      // Send to backend for processing
      submitCapturedImage(imageData);
    }
  };

  const submitCapturedImage = async (imageData) => {
    // API call to backend
    console.log('Submitting image to backend...');
    // await fetch('/api/face-capture', { method: 'POST', body: { image: imageData } });
  };

  const resetCapture = () => {
    setCapturedImage(null);
    setCapturedImage(null);
  };

  return (
    <div className="live-capture">
      <div className="page-header">
        <h2 className="page-title">Live Face Capture</h2>
        <p className="page-description">
          Capture high-quality facial images for identity verification
        </p>
      </div>

      <div className="capture-container">
        {/* Main Capture Area */}
        <div className="capture-main">
          <div className="card capture-card">
            {!isCapturing && !capturedImage && (
              <div className="capture-start">
                <div className="start-icon-wrapper">
                  <Camera size={64} className="start-icon" />
                  <div className="icon-pulse"></div>
                </div>
                <h3>Ready to Capture</h3>
                <p>Position your face in the frame and follow the on-screen guidance</p>
                <button 
                  className="button-primary"
                  onClick={() => setIsCapturing(true)}
                >
                  <Camera size={20} />
                  Start Camera
                </button>
              </div>
            )}

            {isCapturing && (
              <div className="video-container">
                <video 
                  ref={videoRef} 
                  autoPlay 
                  playsInline 
                  muted
                  className="video-feed"
                />
                
                {/* Face Detection Overlay */}
                <div className="face-overlay">
                  <svg className="face-guide" viewBox="0 0 300 400">
                    <ellipse 
                      cx="150" 
                      cy="180" 
                      rx="110" 
                      ry="140"
                      fill="none"
                      stroke={faceDetected ? '#00ff88' : '#00d9ff'}
                      strokeWidth="3"
                      strokeDasharray="10,5"
                      className={faceDetected ? 'detected' : 'detecting'}
                    />
                    
                    {/* Corner markers */}
                    <path d="M 40 40 L 40 80 M 40 40 L 80 40" stroke="#00d9ff" strokeWidth="2" />
                    <path d="M 260 40 L 260 80 M 260 40 L 220 40" stroke="#00d9ff" strokeWidth="2" />
                    <path d="M 40 360 L 40 320 M 40 360 L 80 360" stroke="#00d9ff" strokeWidth="2" />
                    <path d="M 260 360 L 260 320 M 260 360 L 220 360" stroke="#00d9ff" strokeWidth="2" />
                  </svg>
                  
                  {faceDetected && (
                    <div className="detection-indicator">
                      <CheckCircle size={24} />
                      <span>Face Detected</span>
                    </div>
                  )}
                </div>

                {/* Capture Controls */}
                <div className="capture-controls">
                  <button 
                    className="control-btn cancel"
                    onClick={() => setIsCapturing(false)}
                  >
                    <X size={20} />
                  </button>
                  
                  <button 
                    className="control-btn capture"
                    onClick={captureFrame}
                    disabled={!faceDetected || qualityScore < 70}
                  >
                    <Circle size={48} />
                  </button>
                  
                  <div className="control-spacer"></div>
                </div>

                <canvas ref={canvasRef} style={{ display: 'none' }} />
              </div>
            )}

            {capturedImage && (
              <div className="captured-preview">
                <img src={capturedImage} alt="Captured face" />
                <div className="preview-actions">
                  <button className="button-secondary" onClick={resetCapture}>
                    Retake
                  </button>
                  <button className="button-primary">
                    <CheckCircle size={20} />
                    Confirm & Process
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Live Metrics */}
          {isCapturing && (
            <div className="metrics-bar">
              <div className="metric-item">
                <span className="metric-label">Face Detection</span>
                <div className="metric-status">
                  {faceDetected ? (
                    <><CheckCircle size={16} className="status-success" /> Active</>
                  ) : (
                    <><AlertCircle size={16} className="status-warning" /> Searching...</>
                  )}
                </div>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Image Quality</span>
                <div className="quality-bar">
                  <div 
                    className="quality-fill" 
                    style={{ 
                      width: `${qualityScore}%`,
                      background: qualityScore >= 70 ? '#00ff88' : '#ff9500'
                    }}
                  />
                  <span className="quality-score">{qualityScore}%</span>
                </div>
              </div>
              
              <div className="metric-item">
                <span className="metric-label">Lighting</span>
                <span className={`metric-value ${qualityScore > 70 ? 'good' : 'poor'}`}>
                  {qualityScore > 70 ? 'Optimal' : 'Adjust'}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Guidance Panel */}
        <div className="guidance-panel">
          <div className="card">
            <h3 className="guidance-title">Capture Guidelines</h3>
            
            <div className="guideline-list">
              <div className="guideline-item">
                <div className="guideline-icon success">
                  <CheckCircle size={20} />
                </div>
                <div className="guideline-content">
                  <h4>Position Your Face</h4>
                  <p>Center your face within the oval guide</p>
                </div>
              </div>
              
              <div className="guideline-item">
                <div className="guideline-icon success">
                  <CheckCircle size={20} />
                </div>
                <div className="guideline-content">
                  <h4>Good Lighting</h4>
                  <p>Ensure face is evenly lit, avoid shadows</p>
                </div>
              </div>
              
              <div className="guideline-item">
                <div className="guideline-icon success">
                  <CheckCircle size={20} />
                </div>
                <div className="guideline-content">
                  <h4>Neutral Expression</h4>
                  <p>Look directly at camera, no glasses</p>
                </div>
              </div>
              
              <div className="guideline-item">
                <div className="guideline-icon success">
                  <CheckCircle size={20} />
                </div>
                <div className="guideline-content">
                  <h4>Stay Still</h4>
                  <p>Hold steady for optimal clarity</p>
                </div>
              </div>
            </div>

            <div className="stats-grid">
              <div className="stat-card">
                <span className="stat-value">98.2%</span>
                <span className="stat-label">Success Rate</span>
              </div>
              <div className="stat-card">
                <span className="stat-value">1,247</span>
                <span className="stat-label">Today's Captures</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveCapture;