import { useState, useEffect } from 'react';
import { Camera, Shield, Users, BarChart3, DollarSign, User, LogIn } from 'lucide-react';
import LiveCapture from './components/LiveCapture';
import LivenessDetection from './components/LivenessDetection';
import FacialRecognition from './components/FacialRecognition';
import DeduplicationDashboard from './components/DeduplicationDashboard';
import Analytics from './components/Analytics';
import UserManagement from './components/UserManagement';
import Login from './components/Login';
import Pricing from './components/Pricing';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('capture');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  const navigation = [
    { id: 'capture', label: 'Live Capture', icon: Camera, description: 'Capture facial data' },
    { id: 'liveness', label: 'Liveness Check', icon: Shield, description: 'Verify user presence' },
    { id: 'recognition', label: 'Face Recognition', icon: User, description: 'Identify & verify' },
    { id: 'deduplication', label: 'Deduplication', icon: Users, description: 'Review duplicates' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, description: 'System insights' },
    { id: 'users', label: 'User Management', icon: Users, description: 'Manage accounts' },
    { id: 'pricing', label: 'Pricing', icon: DollarSign, description: 'View plans' }
  ];

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setCurrentUser(userData);
    setShowLogin(false);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    setActiveTab('capture');
  };

  const renderContent = () => {
    switch(activeTab) {
      case 'capture':
        return <LiveCapture />;
      case 'liveness':
        return <LivenessDetection />;
      case 'recognition':
        return <FacialRecognition />;
      case 'deduplication':
        return <DeduplicationDashboard />;
      case 'analytics':
        return <Analytics />;
      case 'users':
        return <UserManagement />;
      case 'pricing':
        return <Pricing />;
      default:
        return <LiveCapture />;
    }
  };

  return (
    <div className="app">
      {/* Animated Background */}
      <div className="background-grid"></div>
      <div className="scan-line"></div>
      
      {/* Header - Compact */}
      <header className="app-header compact">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">
              <Shield className="shield-icon" />
            </div>
            <div className="logo-text">
              <h1>KYCVerifyAI</h1>
            </div>
          </div>
          
          <div className="header-actions">
            {!isAuthenticated ? (
              <>
                <button className="auth-btn" onClick={() => setShowLogin(true)}>
                  <LogIn size={16} />
                  Login / Sign Up
                </button>
              </>
            ) : (
              <>
                <div className="user-info-compact">
                  <div className="user-avatar-compact">
                    <User size={14} />
                  </div>
                  <span className="user-name-compact">{currentUser?.name || 'User'}</span>
                </div>
                <button className="logout-btn-compact" onClick={handleLogout}>
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="app-container">
        {/* Sidebar Navigation */}
        <nav className="sidebar">
          <div className="nav-items">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(item.id)}
                >
                  <Icon className="nav-icon" />
                  <div className="nav-text">
                    <span className="nav-label">{item.label}</span>
                  </div>
                  {activeTab === item.id && <div className="active-indicator"></div>}
                </button>
              );
            })}
          </div>
          
          <div className="sidebar-footer">
            <div className="status-indicator">
              <div className="status-dot"></div>
              <span>System Active</span>
            </div>
          </div>
        </nav>

        {/* Content Area */}
        <main className="main-content">
          {renderContent()}
        </main>
      </div>

      {/* Login Modal */}
      {showLogin && (
        <Login 
          onClose={() => setShowLogin(false)} 
          onLogin={handleLogin}
        />
      )}
    </div>
  );
}

export default App;