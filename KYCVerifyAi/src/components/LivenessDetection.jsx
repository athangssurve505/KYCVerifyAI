import { useState, useEffect } from 'react';
import { Eye, Smile, RotateCcw, CheckCircle, XCircle, Play } from 'lucide-react';
import './LivenessDetection.css';

const LivenessDetection = () => {
  const [testActive, setTestActive] = useState(false);
  const [currentChallenge, setCurrentChallenge] = useState(null);
  const [challengeIndex, setChallengeIndex] = useState(0);
  const [results, setResults] = useState([]);
  const [testComplete, setTestComplete] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(5);

  const challenges = [
    { id: 'blink', icon: Eye, label: 'Blink Your Eyes', instruction: 'Blink 2 times naturally' },
    { id: 'smile', icon: Smile, label: 'Smile', instruction: 'Show a natural smile' },
    { id: 'turn-left', icon: RotateCcw, label: 'Turn Left', instruction: 'Turn your head left slowly' },
    { id: 'turn-right', icon: RotateCcw, label: 'Turn Right', instruction: 'Turn your head right slowly' }
  ];

  useEffect(() => {
    if (testActive && currentChallenge && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (timeRemaining === 0 && currentChallenge) {
      completeChallenge();
    }
  }, [testActive, timeRemaining, currentChallenge]);

  const startTest = () => {
    setTestActive(true);
    setResults([]);
    setTestComplete(false);
    setChallengeIndex(0);
    setCurrentChallenge(challenges[0]);
    setTimeRemaining(5);
  };

  const completeChallenge = () => {
    const success = Math.random() > 0.2; // Simulate detection
    setResults([...results, { ...currentChallenge, success }]);
    
    if (challengeIndex < challenges.length - 1) {
      setChallengeIndex(challengeIndex + 1);
      setCurrentChallenge(challenges[challengeIndex + 1]);
      setTimeRemaining(5);
    } else {
      setTestActive(false);
      setTestComplete(true);
      setCurrentChallenge(null);
    }
  };

  const resetTest = () => {
    setTestActive(false);
    setCurrentChallenge(null);
    setChallengeIndex(0);
    setResults([]);
    setTestComplete(false);
    setTimeRemaining(5);
  };

  const successRate = results.length > 0 
    ? (results.filter(r => r.success).length / results.length * 100).toFixed(0)
    : 0;

  const Icon = currentChallenge?.icon;

  return (
    <div className="liveness-detection">
      <div className="page-header">
        <h2 className="page-title">Liveness Detection</h2>
        <p className="page-description">
          Verify user presence with interactive challenges to prevent spoofing attacks
        </p>
      </div>

      <div className="liveness-container">
        {/* Test Area */}
        <div className="test-main">
          <div className="card test-card">
            {!testActive && !testComplete && (
              <div className="test-ready">
                <div className="ready-icon-wrapper">
                  <Shield className="ready-icon" />
                </div>
                <h3>Ready for Liveness Check</h3>
                <p>Complete a series of interactive challenges to verify your presence</p>
                <button className="button-primary" onClick={startTest}>
                  <Play size={20} />
                  Start Liveness Test
                </button>
              </div>
            )}

            {testActive && currentChallenge && (
              <div className="challenge-active">
                <div className="challenge-header">
                  <div className="challenge-progress">
                    <span className="progress-text">
                      Challenge {challengeIndex + 1} of {challenges.length}
                    </span>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${((challengeIndex + 1) / challenges.length) * 100}%` }}
                      />
                    </div>
                  </div>
                  
                  <div className="challenge-timer">
                    <div className="timer-ring">
                      <svg viewBox="0 0 100 100">
                        <circle 
                          cx="50" 
                          cy="50" 
                          r="45"
                          fill="none"
                          stroke="rgba(255,255,255,0.1)"
                          strokeWidth="8"
                        />
                        <circle 
                          cx="50" 
                          cy="50" 
                          r="45"
                          fill="none"
                          stroke="#00d9ff"
                          strokeWidth="8"
                          strokeDasharray={`${(timeRemaining / 5) * 283} 283`}
                          transform="rotate(-90 50 50)"
                          className="timer-circle"
                        />
                      </svg>
                      <span className="timer-value">{timeRemaining}s</span>
                    </div>
                  </div>
                </div>

                <div className="challenge-content">
                  <div className="challenge-icon-large">
                    {Icon && <Icon size={80} />}
                  </div>
                  <h3 className="challenge-label">{currentChallenge.label}</h3>
                  <p className="challenge-instruction">{currentChallenge.instruction}</p>
                  
                  <div className="challenge-visual">
                    <div className="face-placeholder">
                      <div className="scanning-line"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {testComplete && (
              <div className="test-results">
                <div className={`result-icon ${successRate >= 75 ? 'success' : 'failed'}`}>
                  {successRate >= 75 ? <CheckCircle size={64} /> : <XCircle size={64} />}
                </div>
                
                <h3>{successRate >= 75 ? 'Liveness Verified' : 'Verification Failed'}</h3>
                <p className="result-score">Success Rate: {successRate}%</p>
                
                <div className="results-list">
                  {results.map((result, index) => (
                    <div key={index} className="result-item">
                      <div className={`result-status ${result.success ? 'success' : 'failed'}`}>
                        {result.success ? <CheckCircle size={20} /> : <XCircle size={20} />}
                      </div>
                      <span>{result.label}</span>
                    </div>
                  ))}
                </div>

                <div className="result-actions">
                  <button className="button-secondary" onClick={resetTest}>
                    Try Again
                  </button>
                  {successRate >= 75 && (
                    <button className="button-primary">
                      Continue to Verification
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Info Panel */}
        <div className="info-panel">
          <div className="card">
            <h3 className="info-title">About Liveness Detection</h3>
            
            <div className="info-section">
              <h4>Why It Matters</h4>
              <p>
                Liveness detection prevents spoofing attacks using photos, videos, 
                or masks by verifying that a real, live person is present.
              </p>
            </div>

            <div className="info-section">
              <h4>Challenge Types</h4>
              <div className="challenge-types">
                {challenges.map((challenge, index) => {
                  const ChallengeIcon = challenge.icon;
                  const completed = results.find(r => r.id === challenge.id);
                  
                  return (
                    <div key={index} className={`challenge-type ${completed ? 'completed' : ''}`}>
                      <ChallengeIcon size={24} />
                      <span>{challenge.label}</span>
                      {completed && (
                        <div className={`completion-badge ${completed.success ? 'success' : 'failed'}`}>
                          {completed.success ? <CheckCircle size={14} /> : <XCircle size={14} />}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="info-section">
              <h4>Security Features</h4>
              <ul className="feature-list">
                <li>Multi-modal biometric analysis</li>
                <li>Random challenge sequences</li>
                <li>Motion and depth detection</li>
                <li>Anti-spoofing algorithms</li>
              </ul>
            </div>

            <div className="stats-panel">
              <div className="stat-item">
                <span className="stat-value">99.7%</span>
                <span className="stat-label">Detection Accuracy</span>
              </div>
              <div className="stat-item">
                <span className="stat-value">&lt;3s</span>
                <span className="stat-label">Avg. Test Time</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Shield component for ready state
const Shield = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
  </svg>
);

export default LivenessDetection;