from typing import Dict, Optional
from datetime import datetime, timedelta
from authlib.integrations.requests_client import OAuth2Session
import uuid


class OAuthManager:
    def __init__(self, db_session):
        self.db = db_session
    
    def generate_authorization_url(
        self,
        connector_config: Dict,
        redirect_uri: str,
        state: Optional[str] = None
    ) -> Dict[str, str]:
        if state is None:
            state = str(uuid.uuid4())
        
        client_id = connector_config.get("client_id")
        auth_url = connector_config.get("auth_url")
        scope = connector_config.get("scope", [])
        
        if isinstance(scope, list):
            scope = " ".join(scope)
        
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        authorization_url = f"{auth_url}?{query_string}"
        
        return {
            "authorization_url": authorization_url,
            "state": state
        }
    
    def exchange_code_for_token(
        self,
        connector_config: Dict,
        code: str,
        redirect_uri: str
    ) -> Dict:
        client_id = connector_config.get("client_id")
        client_secret = connector_config.get("client_secret")
        token_url = connector_config.get("token_url")
        
        client = OAuth2Session(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri
        )
        
        token = client.fetch_token(
            token_url,
            grant_type="authorization_code",
            code=code
        )
        
        return token
    
    def refresh_access_token(
        self,
        connector_config: Dict,
        refresh_token: str
    ) -> Dict:
        client_id = connector_config.get("client_id")
        client_secret = connector_config.get("client_secret")
        token_url = connector_config.get("token_url")
        
        client = OAuth2Session(
            client_id=client_id,
            client_secret=client_secret
        )
        
        token = client.fetch_token(
            token_url,
            grant_type="refresh_token",
            refresh_token=refresh_token
        )
        
        return token
    
    def is_token_expired(self, expires_at: datetime) -> bool:
        if not expires_at:
            return False
        return datetime.utcnow() >= expires_at
    
    def calculate_expiry(self, expires_in: int) -> datetime:
        return datetime.utcnow() + timedelta(seconds=expires_in)
