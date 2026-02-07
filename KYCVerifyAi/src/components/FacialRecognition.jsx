import { useState } from 'react';
import { Upload, Search, UserCheck, AlertTriangle, CheckCircle } from 'lucide-react';
import './FacialRecognition.css';

const FacialRecognition = () => {
  const [mode, setMode] = useState('verify'); // 'verify' or 'identify'
  const [uploadedImage, setUploadedImage] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setUploadedImage(event.target.result);
        processImage(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const processImage = async (imageData) => {
    setIsProcessing(true);
    setResult(null);
    
    // Simulate processing
    setTimeout(() => {
      if (mode === 'verify') {
        setResult({
          match: Math.random() > 0.3,
          confidence: (Math.random() * 20 + 80).toFixed(2),
          user: {
            name: 'John Smith',
            id: 'USR-2024-1247',
            registered: '2024-01-15'
          }
        });
      } else {
        setResult({
          match: Math.random() > 0.2,
          confidence: (Math.random() * 15 + 85).toFixed(2),
          matches: [
            { name: 'John Smith', id: 'USR-2024-1247', similarity: 96.8 },
            { name: 'Jane Doe', id: 'USR-2024-0892', similarity: 87.3 }
          ]
        });
      }
      setIsProcessing(false);
    }, 2000);
  };

  return (
    <div className="facial-recognition">
      <div className="page-header">
        <h2 className="page-title">Facial Recognition</h2>
        <p className="page-description">
          Verify identity or identify individuals from facial images
        </p>
      </div>

      <div className="recognition-controls">
        <button 
          className={`mode-btn ${mode === 'verify' ? 'active' : ''}`}
          onClick={() => setMode('verify')}
        >
          <UserCheck size={20} />
          <div>
            <span className="mode-label">Verify Identity</span>
            <span className="mode-desc">1:1 match verification</span>
          </div>
        </button>
        <button 
          className={`mode-btn ${mode === 'identify' ? 'active' : ''}`}
          onClick={() => setMode('identify')}
        >
          <Search size={20} />
          <div>
            <span className="mode-label">Identify Person</span>
            <span className="mode-desc">1:N database search</span>
          </div>
        </button>
      </div>

      <div className="recognition-container">
        <div className="upload-section">
          <div className="card upload-card">
            {!uploadedImage ? (
              <label className="upload-area">
                <Upload size={48} className="upload-icon" />
                <h3>Upload Facial Image</h3>
                <p>Drag & drop or click to select</p>
                <span className="upload-formats">JPG, PNG, WEBP (Max 10MB)</span>
                <input 
                  type="file" 
                  accept="image/*" 
                  onChange={handleImageUpload}
                  hidden 
                />
              </label>
            ) : (
              <div className="image-preview">
                <img src={uploadedImage} alt="Uploaded" />
                <button 
                  className="remove-btn"
                  onClick={() => {
                    setUploadedImage(null);
                    setResult(null);
                  }}
                >
                  Remove
                </button>
              </div>
            )}
          </div>

          {isProcessing && (
            <div className="processing-indicator">
              <div className="spinner"></div>
              <span>Processing image...</span>
            </div>
          )}

          {result && !isProcessing && (
            <div className="card result-card">
              <div className={`result-header ${result.match ? 'success' : 'failed'}`}>
                {result.match ? <CheckCircle size={32} /> : <AlertTriangle size={32} />}
                <div>
                  <h3>{result.match ? (mode === 'verify' ? 'Verified' : 'Match Found') : 'No Match'}</h3>
                  <p>Confidence: {result.confidence}%</p>
                </div>
              </div>

              {mode === 'verify' && result.match && (
                <div className="user-details">
                  <div className="detail-row">
                    <span className="label">Name:</span>
                    <span className="value">{result.user.name}</span>
                  </div>
                  <div className="detail-row">
                    <span className="label">User ID:</span>
                    <span className="value monospace">{result.user.id}</span>
                  </div>
                  <div className="detail-row">
                    <span className="label">Registered:</span>
                    <span className="value">{result.user.registered}</span>
                  </div>
                </div>
              )}

              {mode === 'identify' && result.matches && (
                <div className="matches-list">
                  <h4>Top Matches</h4>
                  {result.matches.map((match, idx) => (
                    <div key={idx} className="match-item">
                      <div className="match-info">
                        <span className="match-name">{match.name}</span>
                        <span className="match-id monospace">{match.id}</span>
                      </div>
                      <div className="match-similarity">
                        {match.similarity.toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        <div className="stats-section">
          <div className="card">
            <h3>Recognition Statistics</h3>
            <div className="stat-grid">
              <div className="stat">
                <span className="stat-value">45,892</span>
                <span className="stat-label">Total Faces</span>
              </div>
              <div className="stat">
                <span className="stat-value">98.7%</span>
                <span className="stat-label">Accuracy Rate</span>
              </div>
              <div className="stat">
                <span className="stat-value">3,247</span>
                <span className="stat-label">Today's Scans</span>
              </div>
              <div className="stat">
                <span className="stat-value">&lt;500ms</span>
                <span className="stat-label">Avg Speed</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3>Best Practices</h3>
            <ul className="practices-list">
              <li>Ensure face is clearly visible</li>
              <li>Avoid shadows and glare</li>
              <li>Use front-facing images</li>
              <li>Minimum resolution: 640x480</li>
              <li>Remove glasses if possible</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FacialRecognition;