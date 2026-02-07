import { useState } from 'react';
import { Search, UserPlus, Edit2, Trash2, CheckCircle, XCircle, Filter } from 'lucide-react';
import './UserManagement.css';

const mockUsers = [
  { id: 'USR-2024-4891', name: 'Michael Johnson', email: 'michael.j@email.com', status: 'verified', registered: '2024-02-01' },
  { id: 'USR-2024-4892', name: 'Sarah Williams', email: 'sarah.w@email.com', status: 'pending', registered: '2024-02-03' },
  { id: 'USR-2024-4893', name: 'Robert Chen', email: 'robert.c@email.com', status: 'verified', registered: '2024-02-05' },
  { id: 'USR-2024-4894', name: 'Emma Davis', email: 'emma.d@email.com', status: 'flagged', registered: '2024-02-06' },
  { id: 'USR-2024-4895', name: 'James Wilson', email: 'james.w@email.com', status: 'verified', registered: '2024-02-07' }
];

const UserManagement = () => {
  const [users, setUsers] = useState(mockUsers);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || user.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const stats = {
    total: users.length,
    verified: users.filter(u => u.status === 'verified').length,
    pending: users.filter(u => u.status === 'pending').length,
    flagged: users.filter(u => u.status === 'flagged').length
  };

  return (
    <div className="user-management">
      <div className="page-header">
        <h2 className="page-title">User Management</h2>
        <p className="page-description">
          Manage user accounts and verification status
        </p>
      </div>

      <div className="stats-summary">
        <div className="summary-card">
          <span className="summary-value">{stats.total}</span>
          <span className="summary-label">Total Users</span>
        </div>
        <div className="summary-card">
          <span className="summary-value" style={{ color: 'var(--accent-green)' }}>{stats.verified}</span>
          <span className="summary-label">Verified</span>
        </div>
        <div className="summary-card">
          <span className="summary-value" style={{ color: 'var(--accent-orange)' }}>{stats.pending}</span>
          <span className="summary-label">Pending</span>
        </div>
        <div className="summary-card">
          <span className="summary-value" style={{ color: 'var(--accent-red)' }}>{stats.flagged}</span>
          <span className="summary-label">Flagged</span>
        </div>
      </div>

      <div className="controls-bar">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search users..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <Filter size={18} />
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="all">All Status</option>
            <option value="verified">Verified</option>
            <option value="pending">Pending</option>
            <option value="flagged">Flagged</option>
          </select>
        </div>

        <button className="button-primary">
          <UserPlus size={18} />
          Add User
        </button>
      </div>

      <div className="users-table card">
        <table>
          <thead>
            <tr>
              <th>User ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th>Registered</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(user => (
              <tr key={user.id}>
                <td className="monospace">{user.id}</td>
                <td className="user-name">{user.name}</td>
                <td>{user.email}</td>
                <td>
                  <span className={`status-badge ${user.status}`}>
                    {user.status === 'verified' && <CheckCircle size={14} />}
                    {user.status === 'flagged' && <XCircle size={14} />}
                    {user.status}
                  </span>
                </td>
                <td>{user.registered}</td>
                <td>
                  <div className="action-buttons">
                    <button className="action-icon" title="Edit">
                      <Edit2 size={16} />
                    </button>
                    <button className="action-icon danger" title="Delete">
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredUsers.length === 0 && (
          <div className="no-results">
            <p>No users found matching your criteria</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserManagement;
