package connector

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

type BaseConnector struct {
	ConnectionID  string
	Config        map[string]interface{}
	ConnectorName string
	BaseURL       string
	PlatformURL   string
}

type ProxyRequest struct {
	ConnectionID   string                 `json:"connection_id"`
	EndpointConfig map[string]interface{} `json:"endpoint_config"`
	Params         map[string]interface{} `json:"params,omitempty"`
	Body           map[string]interface{} `json:"body,omitempty"`
	PathParams     map[string]interface{} `json:"path_params,omitempty"`
}

type APIResponse struct {
	Success    bool                   `json:"success"`
	StatusCode int                    `json:"status_code,omitempty"`
	Data       map[string]interface{} `json:"data,omitempty"`
	Error      string                 `json:"error,omitempty"`
}

func NewBaseConnector(connectionID string, config map[string]interface{}) *BaseConnector {
	platformURL, ok := config["platform_url"].(string)
	if !ok {
		platformURL = "http://localhost:5000"
	}

	return &BaseConnector{
		ConnectionID: connectionID,
		Config:       config,
		PlatformURL:  platformURL,
	}
}

func (bc *BaseConnector) ExecuteRequest(
	endpointConfig map[string]interface{},
	params map[string]interface{},
	body map[string]interface{},
	pathParams map[string]interface{},
) (map[string]interface{}, error) {
	proxyURL := fmt.Sprintf("%s/api/v1/proxy/execute", bc.PlatformURL)

	proxyReq := ProxyRequest{
		ConnectionID:   bc.ConnectionID,
		EndpointConfig: endpointConfig,
		Params:         params,
		Body:           body,
		PathParams:     pathParams,
	}

	jsonData, err := json.Marshal(proxyReq)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Post(proxyURL, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	var apiResp APIResponse
	if err := json.Unmarshal(bodyBytes, &apiResp); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}

	if !apiResp.Success {
		return nil, fmt.Errorf("API error: %s", apiResp.Error)
	}

	return apiResp.Data, nil
}

func (bc *BaseConnector) GetConnectionInfo() (map[string]interface{}, error) {
	url := fmt.Sprintf("%s/api/v1/connections/%s", bc.PlatformURL, bc.ConnectionID)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	return result, nil
}
