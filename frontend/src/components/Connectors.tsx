import { useEffect, useState } from 'react';
import { connectorsApi, type ConnectorSummary, type Connector } from '../api/client';

export default function Connectors() {
  const [connectors, setConnectors] = useState<ConnectorSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedConnector, setSelectedConnector] = useState<Connector | null>(null);

  useEffect(() => {
    loadConnectors();
  }, []);

  const loadConnectors = async () => {
    try {
      setLoading(true);
      const data = await connectorsApi.listConnectors();
      setConnectors(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load connectors');
    } finally {
      setLoading(false);
    }
  };

  const handleConnectorClick = async (connectorName: string) => {
    try {
      const connector = await connectorsApi.getConnector(connectorName);
      setSelectedConnector(connector);
    } catch (err: any) {
      setError(err.message || 'Failed to load connector details');
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <p>Loading connectors...</p>
      </div>
    );
  }

  return (
    <>
      <div className="content-header">
        <h2>Available Connectors</h2>
        <p>Browse and explore integration connectors</p>
      </div>
      <div className="content-body">
        {error && (
          <div className="alert alert-error">{error}</div>
        )}
        
        {connectors.length === 0 ? (
          <div className="empty-state">
            <h3>No connectors available</h3>
            <p>Contact your administrator to add connectors</p>
          </div>
        ) : (
          <div className="grid">
            {connectors.map((connector) => (
              <div
                key={connector.name}
                className="connector-card"
                onClick={() => handleConnectorClick(connector.name)}
              >
                <h4>{connector.display_name}</h4>
                <p>{connector.description}</p>
                <div style={{ marginTop: '1rem' }}>
                  <span className="badge badge-info">{connector.auth_type}</span>
                  <span className="badge badge-info" style={{ marginLeft: '0.5rem' }}>
                    v{connector.version}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedConnector && (
        <div className="modal-overlay" onClick={() => setSelectedConnector(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedConnector.display_name}</h3>
            </div>
            <div>
              <p style={{ marginBottom: '1rem', color: '#64748b' }}>
                {selectedConnector.description}
              </p>
              
              <div style={{ marginBottom: '1rem' }}>
                <strong>Base URL:</strong>
                <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
                  {selectedConnector.base_url}
                </p>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <strong>Authentication:</strong>
                <p style={{ color: '#64748b', fontSize: '0.875rem' }}>
                  {selectedConnector.auth.type.toUpperCase()}
                </p>
              </div>

              <div>
                <strong>Endpoints ({selectedConnector.endpoints.length}):</strong>
                <div className="endpoint-list">
                  {selectedConnector.endpoints.map((endpoint) => (
                    <div key={endpoint.name} className="endpoint-item">
                      <div>
                        <span className={`method-badge method-${endpoint.method.toLowerCase()}`}>
                          {endpoint.method}
                        </span>
                        <strong>{endpoint.display_name}</strong>
                        <p style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
                          {endpoint.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button
                className="btn btn-secondary"
                onClick={() => setSelectedConnector(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
