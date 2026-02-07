import { useState } from 'react';
import { X, User, Mail, Lock, Eye, EyeOff } from 'lucide-react';
import './Login.css';

const Login = ({ onClose, onLogin }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Simulate authentication
    if (isSignUp) {
      if (formData.password !== formData.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }
      // Simulate signup
      onLogin({
        name: formData.name,
        email: formData.email
      });
    } else {
      // Simulate login
      onLogin({
        name: formData.email.split('@')[0],
        email: formData.email
      });
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="login-modal-overlay" onClick={onClose}>
      <div className="login-modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="login-close-btn" onClick={onClose}>
          <X size={24} />
        </button>

        <div className="login-header">
          <div className="login-logo">
            <div className="login-logo-icon">
              <User size={32} />
            </div>
            <h2>{isSignUp ? 'Create Account' : 'Welcome Back'}</h2>
            <p>{isSignUp ? 'Sign up to get started' : 'Sign in to continue'}</p>
          </div>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          {isSignUp && (
            <div className="form-group">
              <label>Full Name</label>
              <div className="input-wrapper">
                <User size={18} />
                <input
                  type="text"
                  name="name"
                  placeholder="John Doe"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
          )}

          <div className="form-group">
            <label>Email Address</label>
            <div className="input-wrapper">
              <Mail size={18} />
              <input
                type="email"
                name="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div className="input-wrapper">
              <Lock size={18} />
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          {isSignUp && (
            <div className="form-group">
              <label>Confirm Password</label>
              <div className="input-wrapper">
                <Lock size={18} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  placeholder="••••••••"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
          )}

          <button type="submit" className="login-submit-btn">
            {isSignUp ? 'Sign Up' : 'Sign In'}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {isSignUp ? 'Already have an account?' : "Don't have an account?"}
            <button 
              className="toggle-mode-btn" 
              onClick={() => setIsSignUp(!isSignUp)}
            >
              {isSignUp ? 'Sign In' : 'Sign Up'}
            </button>
          </p>
        </div>

        <div className="login-demo-note">
          <p>💡 <strong>Demo Mode:</strong> Use any email/password to login</p>
        </div>
      </div>
    </div>
  );
};

export default Login;