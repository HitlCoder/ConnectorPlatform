import { useEffect, useState } from 'react';
import { connectionsApi, connectorsApi, oauthApi, type Connection, type ConnectorSummary } from '../api/client';

const USER_ID = 'demo-user';

export default function Connections() {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [connectors, setConnectors] = useState<ConnectorSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newConnection, setNewConnection] = useState({
    connector_type: '',
    name: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [connectionsData, connectorsData] = await Promise.all([
        connectionsApi.listConnections(USER_ID),
        connectorsApi.listConnectors(),
      ]);
      setConnections(connectionsData);
      setConnectors(connectorsData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateConnection = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const connection = await connectionsApi.createConnection({
        ...newConnection,
        user_id: USER_ID,
      });

      const redirectUri = `${window.location.origin}/oauth/callback`;
      const oauthResponse = await oauthApi.initiateOAuth({
        connector_type: newConnection.connector_type,
        connection_id: connection.id,
        redirect_uri: redirectUri,
      });

      localStorage.setItem('oauth_state', oauthResponse.state);
      localStorage.setItem('oauth_connection_id', connection.id);
      localStorage.setItem('oauth_redirect_uri', redirectUri);

      window.location.href = oauthResponse.authorization_url;
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to create connection');
    }
  };

  const handleDeleteConnection = async (id: string) => {
    if (!confirm('Are you sure you want to delete this connection?')) {
      return;
    }

    try {
      await connectionsApi.deleteConnection(id);
      setSuccess('Connection deleted successfully');
      setTimeout(() => setSuccess(null), 3000);
      loadData();
    } catch (err: any) {
      setError(err.message || 'Failed to delete connection');
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <p>Loading connections...</p>
      </div>
    );
  }

  return (
    <>
      <div className="content-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>My Connections</h2>
            <p>Manage your connector integrations</p>
          </div>
          <button
            className="btn btn-primary"
            onClick={() => setShowCreateModal(true)}
          >
            + New Connection
          </button>
        </div>
      </div>
      <div className="content-body">
        {error && (
          <div className="alert alert-error">{error}</div>
        )}
        {success && (
          <div className="alert alert-success">{success}</div>
        )}
        
        {connections.length === 0 ? (
          <div className="empty-state">
            <h3>No connections yet</h3>
            <p>Create your first connection to get started</p>
            <button
              className="btn btn-primary"
              style={{ marginTop: '1rem' }}
              onClick={() => setShowCreateModal(true)}
            >
              + New Connection
            </button>
          </div>
        ) : (
          <div className="grid">
            {connections.map((connection) => (
              <div key={connection.id} className="connection-card">
                <h4>{connection.name}</h4>
                <p>Connector: {connection.connector_type}</p>
                <p style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                  Created: {new Date(connection.created_at).toLocaleDateString()}
                </p>
                <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  <span className={`badge ${connection.status === 'active' ? 'badge-success' : 'badge-warning'}`}>
                    {connection.status}
                  </span>
                  <button
                    className="btn btn-danger"
                    style={{ marginLeft: 'auto', fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteConnection(connection.id);
                    }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Create New Connection</h3>
            </div>
            <form onSubmit={handleCreateConnection}>
              <div className="form-group">
                <label>Connector</label>
                <select
                  required
                  value={newConnection.connector_type}
                  onChange={(e) => setNewConnection({ ...newConnection, connector_type: e.target.value })}
                >
                  <option value="">Select a connector...</option>
                  {connectors.map((connector) => (
                    <option key={connector.name} value={connector.name}>
                      {connector.display_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Connection Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g., My Gmail Account"
                  value={newConnection.name}
                  onChange={(e) => setNewConnection({ ...newConnection, name: e.target.value })}
                />
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create & Authorize
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
