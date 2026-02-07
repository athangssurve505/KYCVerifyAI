import { useState, useEffect } from 'react';
import { Camera, Shield, Users, BarChart3, CheckCircle, AlertTriangle, User, LogOut } from 'lucide-react';
import LiveCapture from './components/LiveCapture';
import LivenessDetection from './components/LivenessDetection';
import FacialRecognition from './components/FacialRecognition';
import DeduplicationDashboard from './components/DeduplicationDashboard';
import Analytics from './components/Analytics';
import UserManagement from './components/UserManagement';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('capture');
  const [isAuthenticated, setIsAuthenticated] = useState(true); // Demo mode
  const [currentUser, setCurrentUser] = useState({
    name: 'Admin User',
    role: 'Security Administrator',
    permissions: ['all']
  });

  const navigation = [
    { id: 'capture', label: 'Live Capture', icon: Camera, description: 'Capture facial data' },
    { id: 'liveness', label: 'Liveness Check', icon: Shield, description: 'Verify user presence' },
    { id: 'recognition', label: 'Face Recognition', icon: User, description: 'Identify & verify' },
    { id: 'deduplication', label: 'Deduplication', icon: Users, description: 'Review duplicates' },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, description: 'System insights' },
    { id: 'users', label: 'User Management', icon: Users, description: 'Manage accounts' }
  ];

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
      default:
        return <LiveCapture />;
    }
  };

  return (
    <div className="app">
      {/* Animated Background */}
      <div className="background-grid"></div>
      <div className="scan-line"></div>
      
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">
              <Shield className="shield-icon" />
            </div>
            <div className="logo-text">
              <h1>SecureID</h1>
              <span className="tagline">Biometric Identity Verification</span>
            </div>
          </div>
          
          <div className="header-actions">
            <div className="user-info">
              <div className="user-avatar">
                <User size={18} />
              </div>
              <div className="user-details">
                <span className="user-name">{currentUser.name}</span>
                <span className="user-role">{currentUser.role}</span>
              </div>
            </div>
            <button className="logout-btn">
              <LogOut size={18} />
            </button>
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
                    <span className="nav-description">{item.description}</span>
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
    </div>
  );
}

export default App;