import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ConnectorSummary {
  name: string;
  display_name: string;
  description: string;
  auth_type: string;
  version: string;
}

export interface Connector {
  name: string;
  display_name: string;
  description: string;
  version: string;
  base_url: string;
  auth: {
    type: string;
    auth_url: string;
    token_url: string;
    scope: string[];
    client_id_env: string;
    client_secret_env: string;
  };
  endpoints: Array<{
    name: string;
    display_name: string;
    description: string;
    method: string;
    path: string;
    parameters?: any[];
    response_type?: string;
  }>;
}

export interface Connection {
  id: string;
  connector_type: string;
  name: string;
  user_id: string;
  status: string;
  config: any;
  created_at: string;
  updated_at: string;
}

export interface OAuthInitResponse {
  authorization_url: string;
  state: string;
  connection_id: string;
}

export const connectorsApi = {
  async listConnectors(): Promise<ConnectorSummary[]> {
    const response = await apiClient.get('/connectors');
    return response.data;
  },

  async getConnector(name: string): Promise<Connector> {
    const response = await apiClient.get(`/connectors/${name}`);
    return response.data;
  },

  async getConnectorEndpoints(name: string) {
    const response = await apiClient.get(`/connectors/${name}/endpoints`);
    return response.data;
  },
};

export const connectionsApi = {
  async listConnections(userId: string): Promise<Connection[]> {
    const response = await apiClient.get('/connections', {
      params: { user_id: userId },
    });
    return response.data;
  },

  async getConnection(id: string): Promise<Connection> {
    const response = await apiClient.get(`/connections/${id}`);
    return response.data;
  },

  async createConnection(data: {
    connector_type: string;
    name: string;
    user_id: string;
    config?: any;
  }): Promise<Connection> {
    const response = await apiClient.post('/connections', data);
    return response.data;
  },

  async deleteConnection(id: string): Promise<void> {
    await apiClient.delete(`/connections/${id}`);
  },
};

export const oauthApi = {
  async initiateOAuth(data: {
    connector_type: string;
    connection_id: string;
    redirect_uri: string;
  }): Promise<OAuthInitResponse> {
    const response = await apiClient.post('/oauth/authorize', data);
    return response.data;
  },

  async completeOAuth(data: {
    connection_id: string;
    code: string;
    state: string;
    redirect_uri: string;
  }) {
    const response = await apiClient.post('/oauth/callback', data);
    return response.data;
  },
};

export const proxyApi = {
  async executeRequest(data: {
    connection_id: string;
    endpoint_config: any;
    params?: any;
    body?: any;
    path_params?: any;
  }) {
    const response = await apiClient.post('/proxy/execute', data);
    return response.data;
  },
};

export default apiClient;
