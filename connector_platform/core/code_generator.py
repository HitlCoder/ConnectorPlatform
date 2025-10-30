from jinja2 import Template
from pathlib import Path
import yaml
from typing import Dict


class CodeGenerator:
    def __init__(self):
        self.template_dir = Path("connector_platform/templates")
        self.template_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_connector_code(self, config: Dict, language: str = "python") -> str:
        if language == "python":
            return self._generate_python_connector(config)
        elif language == "go":
            return self._generate_go_connector(config)
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def _generate_python_connector(self, config: Dict) -> str:
        template_str = '''"""
{{ display_name }} Connector
Generated from configuration
"""
from sdk.python.base_connector import BaseConnector
from typing import Dict, List, Optional, Any


class {{ class_name }}Connector(BaseConnector):
    """{{ description }}"""
    
    def __init__(self, connection_id: str, config: Dict):
        super().__init__(connection_id, config)
        self.connector_name = "{{ name }}"
        self.base_url = "{{ base_url }}"
    
{% for endpoint in endpoints %}
    def {{ endpoint.name }}(self{% for param in endpoint.parameters %}, {{ param.name }}: {{ param.type }}{% if not param.required %} = None{% endif %}{% endfor %}) -> Dict[str, Any]:
        """
        {{ endpoint.description }}
        
        Args:
{% for param in endpoint.parameters %}
            {{ param.name }}: {{ param.description }}
{% endfor %}
        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "{{ endpoint.method }}",
            "path": "{{ endpoint.path }}",
            "headers": {{ endpoint.headers }}
        }
        
        params = {}
        body = {}
        path_params = {}
        
{% for param in endpoint.parameters %}
        {% if param.location == "query" %}
        if {{ param.name }} is not None:
            params["{{ param.name }}"] = {{ param.name }}
        {% elif param.location == "body" %}
        if {{ param.name }} is not None:
            body["{{ param.name }}"] = {{ param.name }}
        {% elif param.location == "path" %}
        if {{ param.name }} is not None:
            path_params["{{ param.name }}"] = {{ param.name }}
        {% endif %}
{% endfor %}
        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )

{% endfor %}
'''
        
        template = Template(template_str)
        
        class_name = "".join(word.capitalize() for word in config["name"].replace("-", "_").split("_"))
        
        return template.render(
            name=config["name"],
            display_name=config["display_name"],
            description=config.get("description", ""),
            class_name=class_name,
            base_url=config["base_url"],
            endpoints=config.get("endpoints", [])
        )
    
    def _generate_go_connector(self, config: Dict) -> str:
        template_str = '''package connectors

import (
    "github.com/connector-platform/sdk/go/connector"
)

// {{ class_name }}Connector implements the {{ display_name }} connector
type {{ class_name }}Connector struct {
    connector.BaseConnector
}

// New{{ class_name }}Connector creates a new {{ display_name }} connector instance
func New{{ class_name }}Connector(connectionID string, config map[string]interface{}) *{{ class_name }}Connector {
    return &{{ class_name }}Connector{
        BaseConnector: connector.BaseConnector{
            ConnectionID: connectionID,
            Config:       config,
            ConnectorName: "{{ name }}",
            BaseURL:      "{{ base_url }}",
        },
    }
}

{% for endpoint in endpoints %}
// {{ endpoint.display_name|replace(" ", "") }} {{ endpoint.description }}
func (c *{{ class_name }}Connector) {{ endpoint.display_name|replace(" ", "") }}({% for param in endpoint.parameters %}{{ param.name }} {{ param.type|go_type }}{% if not loop.last %}, {% endif %}{% endfor %}) (map[string]interface{}, error) {
    endpointConfig := map[string]interface{}{
        "method": "{{ endpoint.method }}",
        "path":   "{{ endpoint.path }}",
        "headers": map[string]string{{ endpoint.headers }},
    }
    
    params := make(map[string]interface{})
    body := make(map[string]interface{})
    pathParams := make(map[string]interface{})
    
{% for param in endpoint.parameters %}
    {% if param.location == "query" %}
    params["{{ param.name }}"] = {{ param.name }}
    {% elif param.location == "body" %}
    body["{{ param.name }}"] = {{ param.name }}
    {% elif param.location == "path" %}
    pathParams["{{ param.name }}"] = {{ param.name }}
    {% endif %}
{% endfor %}
    
    return c.ExecuteRequest(endpointConfig, params, body, pathParams)
}

{% endfor %}
'''
        
        template = Template(template_str)
        template.filters['go_type'] = lambda x: {"str": "string", "int": "int", "bool": "bool", "dict": "map[string]interface{}", "list": "[]interface{}"}.get(x, "interface{}")
        
        class_name = "".join(word.capitalize() for word in config["name"].replace("-", "_").split("_"))
        
        return template.render(
            name=config["name"],
            display_name=config["display_name"],
            description=config.get("description", ""),
            class_name=class_name,
            base_url=config["base_url"],
            endpoints=config.get("endpoints", [])
        )
    
    def save_generated_code(
        self,
        code: str,
        connector_name: str,
        language: str = "python"
    ):
        if language == "python":
            output_dir = Path(f"platform/connectors")
            output_dir.mkdir(parents=True, exist_ok=True)
            file_path = output_dir / f"{connector_name}_connector.py"
        elif language == "go":
            output_dir = Path(f"platform/connectors/go")
            output_dir.mkdir(parents=True, exist_ok=True)
            file_path = output_dir / f"{connector_name}_connector.go"
        else:
            raise ValueError(f"Unsupported language: {language}")
        
        with open(file_path, 'w') as f:
            f.write(code)
        
        return str(file_path)
