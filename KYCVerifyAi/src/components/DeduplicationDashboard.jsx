import { useState } from 'react';
import { Users, AlertTriangle, CheckCircle, X, Eye } from 'lucide-react';
import './DeduplicationDashboard.css';

const mockDuplicates = [
  {
    id: 1,
    primary: { name: 'Michael Johnson', id: 'USR-2024-3891', image: null, registered: '2024-01-10' },
    duplicate: { name: 'Mike Johnson', id: 'USR-2024-4127', image: null, registered: '2024-02-03' },
    similarity: 97.8,
    status: 'pending'
  },
  {
    id: 2,
    primary: { name: 'Sarah Williams', id: 'USR-2024-2145', image: null, registered: '2023-11-22' },
    duplicate: { name: 'Sara Williams', id: 'USR-2024-4892', image: null, registered: '2024-01-28' },
    similarity: 96.3,
    status: 'pending'
  },
  {
    id: 3,
    primary: { name: 'Robert Chen', id: 'USR-2023-8763', image: null, registered: '2023-08-15' },
    duplicate: { name: 'Rob Chen', id: 'USR-2024-1009', image: null, registered: '2024-01-05' },
    similarity: 95.1,
    status: 'pending'
  }
];

const DeduplicationDashboard = () => {
  const [duplicates, setDuplicates] = useState(mockDuplicates);
  const [selectedItem, setSelectedItem] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all', 'high', 'medium'

  const handleAction = (id, action) => {
    setDuplicates(duplicates.map(d => 
      d.id === id ? { ...d, status: action } : d
    ));
    setSelectedItem(null);
  };

  const getSimilarityLevel = (similarity) => {
    if (similarity >= 95) return 'high';
    if (similarity >= 90) return 'medium';
    return 'low';
  };

  const filteredDuplicates = duplicates.filter(d => {
    if (filter === 'all') return d.status === 'pending';
    const level = getSimilarityLevel(d.similarity);
    return level === filter && d.status === 'pending';
  });

  const stats = {
    total: duplicates.filter(d => d.status === 'pending').length,
    resolved: duplicates.filter(d => d.status !== 'pending').length,
    high: duplicates.filter(d => getSimilarityLevel(d.similarity) === 'high' && d.status === 'pending').length
  };

  return (
    <div className="deduplication-dashboard">
      <div className="page-header">
        <h2 className="page-title">Deduplication Dashboard</h2>
        <p className="page-description">
          Review and resolve potential duplicate facial records
        </p>
      </div>

      <div className="stats-bar">
        <div className="stat-box">
          <AlertTriangle className="stat-icon warning" />
          <div>
            <span className="stat-value">{stats.total}</span>
            <span className="stat-label">Pending Review</span>
          </div>
        </div>
        <div className="stat-box">
          <CheckCircle className="stat-icon success" />
          <div>
            <span className="stat-value">{stats.resolved}</span>
            <span className="stat-label">Resolved</span>
          </div>
        </div>
        <div className="stat-box">
          <Users className="stat-icon primary" />
          <div>
            <span className="stat-value">{stats.high}</span>
            <span className="stat-label">High Confidence</span>
          </div>
        </div>
      </div>

      <div className="filters">
        <button className={`filter-btn ${filter === 'all' ? 'active' : ''}`} onClick={() => setFilter('all')}>
          All
        </button>
        <button className={`filter-btn ${filter === 'high' ? 'active' : ''}`} onClick={() => setFilter('high')}>
          High (&gt;95%)
        </button>
        <button className={`filter-btn ${filter === 'medium' ? 'active' : ''}`} onClick={() => setFilter('medium')}>
          Medium (90-95%)
        </button>
      </div>

      <div className="duplicates-list">
        {filteredDuplicates.map(item => (
          <div key={item.id} className="duplicate-card card">
            <div className="duplicate-header">
              <div className={`similarity-badge ${getSimilarityLevel(item.similarity)}`}>
                {item.similarity.toFixed(1)}% Match
              </div>
              <button className="view-btn" onClick={() => setSelectedItem(item)}>
                <Eye size={18} />
                Review
              </button>
            </div>

            <div className="duplicate-content">
              <div className="user-panel">
                <div className="user-avatar">{item.primary.name.charAt(0)}</div>
                <div className="user-info">
                  <h4>{item.primary.name}</h4>
                  <span className="user-id monospace">{item.primary.id}</span>
                  <span className="user-date">Registered: {item.primary.registered}</span>
                </div>
              </div>

              <div className="duplicate-arrow">⟷</div>

              <div className="user-panel">
                <div className="user-avatar">{item.duplicate.name.charAt(0)}</div>
                <div className="user-info">
                  <h4>{item.duplicate.name}</h4>
                  <span className="user-id monospace">{item.duplicate.id}</span>
                  <span className="user-date">Registered: {item.duplicate.registered}</span>
                </div>
              </div>
            </div>

            <div className="duplicate-actions">
              <button 
                className="action-btn merge"
                onClick={() => handleAction(item.id, 'merged')}
              >
                <CheckCircle size={16} />
                Merge Records
              </button>
              <button 
                className="action-btn keep-both"
                onClick={() => handleAction(item.id, 'kept-separate')}
              >
                <Users size={16} />
                Keep Separate
              </button>
            </div>
          </div>
        ))}

        {filteredDuplicates.length === 0 && (
          <div className="empty-state">
            <CheckCircle size={48} className="empty-icon" />
            <h3>All Clear!</h3>
            <p>No pending duplicates to review</p>
          </div>
        )}
      </div>

      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          <div className="modal-content card" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedItem(null)}>
              <X size={24} />
            </button>
            <h3>Detailed Review</h3>
            <div className="modal-details">
              <p>Similarity Score: <strong>{selectedItem.similarity}%</strong></p>
              <p>Detection Date: <strong>{new Date().toLocaleDateString()}</strong></p>
              <div className="comparison-grid">
                <div>
                  <h4>Primary Record</h4>
                  <p>Name: {selectedItem.primary.name}</p>
                  <p>ID: {selectedItem.primary.id}</p>
                  <p>Registered: {selectedItem.primary.registered}</p>
                </div>
                <div>
                  <h4>Potential Duplicate</h4>
                  <p>Name: {selectedItem.duplicate.name}</p>
                  <p>ID: {selectedItem.duplicate.id}</p>
                  <p>Registered: {selectedItem.duplicate.registered}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DeduplicationDashboard;