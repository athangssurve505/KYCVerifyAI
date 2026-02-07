import { TrendingUp, Users, Shield, Activity } from 'lucide-react';
import './Analytics.css';

const Analytics = () => {
  const metrics = [
    { label: 'Total Scans', value: '124,892', change: '+12.5%', trend: 'up' },
    { label: 'Unique Users', value: '45,231', change: '+8.3%', trend: 'up' },
    { label: 'Success Rate', value: '98.7%', change: '+0.4%', trend: 'up' },
    { label: 'Fraud Prevented', value: '1,247', change: '-5.2%', trend: 'down' }
  ];

  const weeklyData = [
    { day: 'Mon', scans: 4200, success: 98.5 },
    { day: 'Tue', scans: 5100, success: 98.8 },
    { day: 'Wed', scans: 4800, success: 98.2 },
    { day: 'Thu', scans: 5500, success: 99.1 },
    { day: 'Fri', scans: 6200, success: 98.9 },
    { day: 'Sat', scans: 3100, success: 97.8 },
    { day: 'Sun', scans: 2800, success: 98.3 }
  ];

  const maxScans = Math.max(...weeklyData.map(d => d.scans));

  return (
    <div className="analytics">
      <div className="page-header">
        <h2 className="page-title">Analytics & Insights</h2>
        <p className="page-description">
          Monitor system performance and security metrics
        </p>
      </div>

      <div className="metrics-grid">
        {metrics.map((metric, idx) => (
          <div key={idx} className="metric-card card">
            <div className="metric-header">
              <span className="metric-label">{metric.label}</span>
              <span className={`metric-change ${metric.trend}`}>
                {metric.change}
              </span>
            </div>
            <div className="metric-value">{metric.value}</div>
            <div className="metric-bar">
              <div className="metric-fill" style={{ width: '70%' }}></div>
            </div>
          </div>
        ))}
      </div>

      <div className="charts-grid">
        <div className="card chart-card">
          <h3>Weekly Activity</h3>
          <div className="bar-chart">
            {weeklyData.map((data, idx) => (
              <div key={idx} className="bar-group">
                <div className="bar-container">
                  <div 
                    className="bar" 
                    style={{ height: `${(data.scans / maxScans) * 100}%` }}
                  >
                    <span className="bar-value">{(data.scans / 1000).toFixed(1)}k</span>
                  </div>
                </div>
                <span className="bar-label">{data.day}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card chart-card">
          <h3>System Health</h3>
          <div className="health-metrics">
            <div className="health-item">
              <div className="health-header">
                <Activity size={20} />
                <span>API Response Time</span>
              </div>
              <div className="health-value">124ms</div>
              <div className="health-bar">
                <div className="health-fill good" style={{ width: '85%' }}></div>
              </div>
            </div>
            <div className="health-item">
              <div className="health-header">
                <Shield size={20} />
                <span>Security Score</span>
              </div>
              <div className="health-value">99.2%</div>
              <div className="health-bar">
                <div className="health-fill good" style={{ width: '99%' }}></div>
              </div>
            </div>
            <div className="health-item">
              <div className="health-header">
                <Users size={20} />
                <span>Database Load</span>
              </div>
              <div className="health-value">67%</div>
              <div className="health-bar">
                <div className="health-fill warning" style={{ width: '67%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="recent-activity card">
        <h3>Recent Activity</h3>
        <div className="activity-list">
          {[
            { type: 'success', msg: 'User verification successful', time: '2 min ago' },
            { type: 'warning', msg: 'Duplicate detected and merged', time: '15 min ago' },
            { type: 'success', msg: 'New user registered', time: '1 hour ago' },
            { type: 'danger', msg: 'Potential fraud blocked', time: '2 hours ago' },
            { type: 'success', msg: 'Liveness check passed', time: '3 hours ago' }
          ].map((activity, idx) => (
            <div key={idx} className="activity-item">
              <div className={`activity-dot ${activity.type}`}></div>
              <div className="activity-content">
                <span className="activity-msg">{activity.msg}</span>
                <span className="activity-time">{activity.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Analytics;