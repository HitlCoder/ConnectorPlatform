package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

type ConnectorPlatformClient struct {
	PlatformURL string
	BaseURL     string
	HTTPClient  *http.Client
}

type Connection struct {
	ID            string                 `json:"id"`
	ConnectorType string                 `json:"connector_type"`
	Name          string                 `json:"name"`
	UserID        string                 `json:"user_id"`
	Status        string                 `json:"status"`
	Config        map[string]interface{} `json:"config"`
}

type OAuthInitResponse struct {
	AuthorizationURL string `json:"authorization_url"`
	State            string `json:"state"`
}

func NewClient(platformURL string) *ConnectorPlatformClient {
	if platformURL == "" {
		platformURL = "http://localhost:5000"
	}

	return &ConnectorPlatformClient{
		PlatformURL: platformURL,
		BaseURL:     fmt.Sprintf("%s/api/v1", platformURL),
		HTTPClient:  &http.Client{Timeout: 30 * time.Second},
	}
}

func (c *ConnectorPlatformClient) ListConnectors() ([]map[string]interface{}, error) {
	url := fmt.Sprintf("%s/connectors", c.BaseURL)
	
	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var connectors []map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&connectors); err != nil {
		return nil, err
	}

	return connectors, nil
}

func (c *ConnectorPlatformClient) CreateConnection(
	connectorType, name, userID string,
	config map[string]interface{},
) (*Connection, error) {
	url := fmt.Sprintf("%s/connections", c.BaseURL)

	payload := map[string]interface{}{
		"connector_type": connectorType,
		"name":           name,
		"user_id":        userID,
		"config":         config,
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	resp, err := c.HTTPClient.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var connection Connection
	if err := json.NewDecoder(resp.Body).Decode(&connection); err != nil {
		return nil, err
	}

	return &connection, nil
}

func (c *ConnectorPlatformClient) GetConnection(connectionID string) (*Connection, error) {
	url := fmt.Sprintf("%s/connections/%s", c.BaseURL, connectionID)

	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var connection Connection
	if err := json.NewDecoder(resp.Body).Decode(&connection); err != nil {
		return nil, err
	}

	return &connection, nil
}

func (c *ConnectorPlatformClient) DeleteConnection(connectionID string) error {
	url := fmt.Sprintf("%s/connections/%s", c.BaseURL, connectionID)

	req, err := http.NewRequest("DELETE", url, nil)
	if err != nil {
		return err
	}

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("delete failed: %s", string(body))
	}

	return nil
}

func (c *ConnectorPlatformClient) InitiateOAuth(
	connectorType, redirectURI string,
) (*OAuthInitResponse, error) {
	url := fmt.Sprintf("%s/oauth/authorize", c.BaseURL)

	payload := map[string]string{
		"connector_type": connectorType,
		"redirect_uri":   redirectURI,
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	resp, err := c.HTTPClient.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result OAuthInitResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return &result, nil
}

func (c *ConnectorPlatformClient) CompleteOAuth(
	connectionID, code, redirectURI string,
) (map[string]interface{}, error) {
	url := fmt.Sprintf("%s/oauth/callback", c.BaseURL)

	payload := map[string]string{
		"connection_id": connectionID,
		"code":          code,
		"redirect_uri":  redirectURI,
	}

	jsonData, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	resp, err := c.HTTPClient.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, err
	}

	return result, nil
}
