import { useEffect, useState } from 'react';
import { connectionsApi, connectorsApi, proxyApi, type Connection, type Connector } from '../api/client';

const USER_ID = 'demo-user';

export default function ApiTester() {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [selectedConnection, setSelectedConnection] = useState<string>('');
  const [connector, setConnector] = useState<Connector | null>(null);
  const [selectedEndpoint, setSelectedEndpoint] = useState<string>('');
  const [parameters, setParameters] = useState<Record<string, any>>({});
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadConnections();
  }, []);

  useEffect(() => {
    if (selectedConnection) {
      loadConnector();
    }
  }, [selectedConnection]);

  const loadConnections = async () => {
    try {
      const data = await connectionsApi.listConnections(USER_ID);
      const activeConnections = data.filter(c => c.status === 'active');
      setConnections(activeConnections);
    } catch (err: any) {
      setError(err.message || 'Failed to load connections');
    }
  };

  const loadConnector = async () => {
    try {
      const connection = connections.find(c => c.id === selectedConnection);
      if (connection) {
        const connectorData = await connectorsApi.getConnector(connection.connector_type);
        setConnector(connectorData);
        setSelectedEndpoint('');
        setParameters({});
        setResponse(null);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load connector');
    }
  };

  const handleExecuteRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const endpoint = connector?.endpoints.find(e => e.name === selectedEndpoint);
      if (!endpoint) {
        throw new Error('Invalid endpoint');
      }

      const result = await proxyApi.executeRequest({
        connection_id: selectedConnection,
        endpoint_config: endpoint,
        params: parameters,
      });

      setResponse(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Request failed');
    } finally {
      setLoading(false);
    }
  };

  const currentEndpoint = connector?.endpoints.find(e => e.name === selectedEndpoint);

  return (
    <>
      <div className="content-header">
        <h2>API Tester</h2>
        <p>Test your connector endpoints</p>
      </div>
      <div className="content-body">
        {connections.length === 0 ? (
          <div className="empty-state">
            <h3>No active connections</h3>
            <p>Create and authorize a connection first</p>
          </div>
        ) : (
          <div className="card">
            <form onSubmit={handleExecuteRequest}>
              <div className="form-group">
                <label>Connection</label>
                <select
                  required
                  value={selectedConnection}
                  onChange={(e) => setSelectedConnection(e.target.value)}
                >
                  <option value="">Select a connection...</option>
                  {connections.map((connection) => (
                    <option key={connection.id} value={connection.id}>
                      {connection.name} ({connection.connector_type})
                    </option>
                  ))}
                </select>
              </div>

              {connector && (
                <div className="form-group">
                  <label>Endpoint</label>
                  <select
                    required
                    value={selectedEndpoint}
                    onChange={(e) => setSelectedEndpoint(e.target.value)}
                  >
                    <option value="">Select an endpoint...</option>
                    {connector.endpoints.map((endpoint) => (
                      <option key={endpoint.name} value={endpoint.name}>
                        {endpoint.display_name} ({endpoint.method})
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {currentEndpoint && currentEndpoint.parameters && currentEndpoint.parameters.length > 0 && (
                <div>
                  <h4 style={{ marginBottom: '1rem' }}>Parameters</h4>
                  {currentEndpoint.parameters.map((param: any) => (
                    <div key={param.name} className="form-group">
                      <label>
                        {param.name} {param.required && <span style={{ color: '#ef4444' }}>*</span>}
                      </label>
                      <input
                        type={param.type === 'int' ? 'number' : 'text'}
                        required={param.required}
                        placeholder={param.description}
                        value={parameters[param.name] || ''}
                        onChange={(e) => setParameters({
                          ...parameters,
                          [param.name]: param.type === 'int' ? parseInt(e.target.value) : e.target.value
                        })}
                      />
                    </div>
                  ))}
                </div>
              )}

              <div style={{ marginTop: '1.5rem' }}>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={!selectedEndpoint || loading}
                >
                  {loading ? 'Executing...' : 'Execute Request'}
                </button>
              </div>
            </form>

            {error && (
              <div className="alert alert-error" style={{ marginTop: '1.5rem' }}>
                {error}
              </div>
            )}

            {response && (
              <div style={{ marginTop: '1.5rem' }}>
                <h4>Response</h4>
                <pre style={{
                  backgroundColor: '#1e293b',
                  color: '#e2e8f0',
                  padding: '1rem',
                  borderRadius: '0.375rem',
                  overflow: 'auto',
                  maxHeight: '400px',
                  fontSize: '0.875rem'
                }}>
                  {JSON.stringify(response, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}
