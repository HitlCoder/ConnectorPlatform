from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
import os

from connector_platform.database import init_db, get_db
from connector_platform.core.oauth_manager import OAuthManager
from connector_platform.core.connection_manager import ConnectionManager
from connector_platform.core.api_proxy import APIProxy
from connector_platform.core.connector_registry import ConnectorRegistry

app = FastAPI(title="Connector Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

registry = ConnectorRegistry()
registry.load_connector_configs()


@app.on_event("startup")
def startup_event():
    init_db()


class CreateConnectionRequest(BaseModel):
    connector_type: str
    name: str
    user_id: str
    config: Optional[dict] = {}


class OAuthAuthorizeRequest(BaseModel):
    connector_type: str
    redirect_uri: str
    connection_id: Optional[str] = None


class OAuthCallbackRequest(BaseModel):
    connection_id: str
    code: str
    redirect_uri: str


class ProxyExecuteRequest(BaseModel):
    connection_id: str
    endpoint_config: dict
    params: Optional[dict] = None
    body: Optional[dict] = None
    path_params: Optional[dict] = None


@app.get("/")
def root():
    return {
        "message": "Connector Platform API",
        "version": "1.0.0",
        "endpoints": {
            "connectors": "/api/v1/connectors",
            "connections": "/api/v1/connections",
            "oauth": "/api/v1/oauth",
            "proxy": "/api/v1/proxy"
        }
    }


@app.get("/api/v1/connectors")
def list_connectors():
    return registry.list_connectors()


@app.get("/api/v1/connectors/{connector_name}")
def get_connector(connector_name: str):
    connector = registry.get_connector(connector_name)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    return connector


@app.get("/api/v1/connectors/{connector_name}/endpoints")
def list_connector_endpoints(connector_name: str):
    endpoints = registry.get_connector_endpoints(connector_name)
    if not endpoints:
        raise HTTPException(status_code=404, detail="Connector not found")
    return endpoints


@app.post("/api/v1/connections")
def create_connection(
    request: CreateConnectionRequest,
    db: Session = Depends(get_db)
):
    connector = registry.get_connector(request.connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    manager = ConnectionManager(db)
    connection = manager.create_connection(
        connector_type=request.connector_type,
        name=request.name,
        user_id=request.user_id,
        config=request.config
    )
    
    return {
        "id": connection.id,
        "connector_type": connection.connector_type,
        "name": connection.name,
        "user_id": connection.user_id,
        "status": connection.status,
        "config": connection.config,
        "created_at": connection.created_at.isoformat()
    }


@app.get("/api/v1/connections/{connection_id}")
def get_connection(connection_id: str, db: Session = Depends(get_db)):
    manager = ConnectionManager(db)
    connection = manager.get_connection(connection_id)
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    return {
        "id": connection.id,
        "connector_type": connection.connector_type,
        "name": connection.name,
        "user_id": connection.user_id,
        "status": connection.status,
        "config": connection.config,
        "created_at": connection.created_at.isoformat(),
        "updated_at": connection.updated_at.isoformat()
    }


@app.get("/api/v1/connections")
def list_connections(
    user_id: str,
    connector_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    manager = ConnectionManager(db)
    connections = manager.list_connections(user_id, connector_type)
    
    return [
        {
            "id": conn.id,
            "connector_type": conn.connector_type,
            "name": conn.name,
            "status": conn.status,
            "created_at": conn.created_at.isoformat()
        }
        for conn in connections
    ]


@app.delete("/api/v1/connections/{connection_id}")
def delete_connection(connection_id: str, db: Session = Depends(get_db)):
    manager = ConnectionManager(db)
    success = manager.delete_connection(connection_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    return {"message": "Connection deleted successfully"}


@app.post("/api/v1/oauth/authorize")
def oauth_authorize(
    request: OAuthAuthorizeRequest,
    db: Session = Depends(get_db)
):
    connector = registry.get_connector(request.connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    auth_config = connector.get("auth", {})
    
    client_id = os.getenv(auth_config.get("client_id_env", ""))
    client_secret = os.getenv(auth_config.get("client_secret_env", ""))
    
    if not client_id or not client_secret:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth credentials not configured. Set {auth_config.get('client_id_env')} and {auth_config.get('client_secret_env')}"
        )
    
    connector_config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_url": auth_config.get("auth_url"),
        "token_url": auth_config.get("token_url"),
        "scope": auth_config.get("scope", [])
    }
    
    oauth_manager = OAuthManager(db)
    result = oauth_manager.generate_authorization_url(
        connector_config,
        request.redirect_uri
    )
    
    if request.connection_id:
        result["connection_id"] = request.connection_id
    
    return result


@app.post("/api/v1/oauth/callback")
def oauth_callback(
    request: OAuthCallbackRequest,
    db: Session = Depends(get_db)
):
    manager = ConnectionManager(db)
    connection = manager.get_connection(request.connection_id)
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    connector = registry.get_connector(connection.connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    auth_config = connector.get("auth", {})
    
    client_id = os.getenv(auth_config.get("client_id_env", ""))
    client_secret = os.getenv(auth_config.get("client_secret_env", ""))
    
    connector_config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "token_url": auth_config.get("token_url")
    }
    
    oauth_manager = OAuthManager(db)
    
    try:
        token_data = oauth_manager.exchange_code_for_token(
            connector_config,
            request.code,
            request.redirect_uri
        )
        
        manager.store_oauth_token(request.connection_id, token_data)
        
        manager.update_connection(request.connection_id, status="active")
        
        return {
            "success": True,
            "message": "OAuth flow completed successfully",
            "connection_id": request.connection_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {str(e)}")


@app.post("/api/v1/proxy/execute")
def proxy_execute(
    request: ProxyExecuteRequest,
    db: Session = Depends(get_db)
):
    manager = ConnectionManager(db)
    connection = manager.get_connection(request.connection_id)
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    connector = registry.get_connector(connection.connector_type)
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    
    auth_config = connector.get("auth", {})
    
    client_id = os.getenv(auth_config.get("client_id_env", ""))
    client_secret = os.getenv(auth_config.get("client_secret_env", ""))
    
    connector_config = {
        "client_id": client_id,
        "client_secret": client_secret,
        "token_url": auth_config.get("token_url"),
        "base_url": connector.get("base_url")
    }
    
    oauth_manager = OAuthManager(db)
    proxy = APIProxy(db, oauth_manager, manager)
    
    result = proxy.execute_request(
        connection_id=request.connection_id,
        connector_config=connector_config,
        endpoint_config=request.endpoint_config,
        params=request.params,
        body=request.body,
        path_params=request.path_params
    )
    
    return result


@app.get("/health")
def health_check():
    return {"status": "healthy"}
