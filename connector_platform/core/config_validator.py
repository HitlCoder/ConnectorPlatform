from typing import Dict, List, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class AuthType(str, Enum):
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BASIC = "basic"


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class ParameterLocation(str, Enum):
    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    BODY = "body"


class ParameterSchema(BaseModel):
    name: str
    type: str
    required: bool = False
    description: str = ""
    location: ParameterLocation = ParameterLocation.QUERY
    default: Any = None


class EndpointSchema(BaseModel):
    name: str
    display_name: str
    description: str = ""
    method: HTTPMethod
    path: str
    parameters: List[ParameterSchema] = []
    headers: Dict[str, str] = {}
    response_type: str = "json"


class OAuthConfigSchema(BaseModel):
    type: AuthType = AuthType.OAUTH2
    auth_url: str
    token_url: str
    scope: List[str] = []
    client_id_env: str = ""
    client_secret_env: str = ""


class ConnectorConfigSchema(BaseModel):
    name: str
    display_name: str
    description: str = ""
    version: str = "1.0.0"
    base_url: str
    auth: OAuthConfigSchema
    endpoints: List[EndpointSchema]
    
    @validator('name')
    def validate_name(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Connector name must be alphanumeric with underscores or hyphens')
        return v.lower()


class ConfigValidator:
    @staticmethod
    def validate_connector_config(config: Dict) -> tuple[bool, List[str]]:
        errors = []
        
        try:
            ConnectorConfigSchema(**config)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors
    
    @staticmethod
    def validate_endpoint_config(endpoint: Dict) -> tuple[bool, List[str]]:
        errors = []
        
        try:
            EndpointSchema(**endpoint)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors
