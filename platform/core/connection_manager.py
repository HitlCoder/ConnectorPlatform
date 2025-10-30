from typing import Dict, List, Optional
from datetime import datetime
import uuid
from platform.database import Connection, OAuthToken


class ConnectionManager:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_connection(
        self,
        connector_type: str,
        name: str,
        user_id: str,
        config: Optional[Dict] = None
    ) -> Connection:
        connection_id = str(uuid.uuid4())
        
        connection = Connection(
            id=connection_id,
            connector_type=connector_type,
            name=name,
            user_id=user_id,
            config=config or {},
            status="pending"
        )
        
        self.db.add(connection)
        self.db.commit()
        self.db.refresh(connection)
        
        return connection
    
    def get_connection(self, connection_id: str) -> Optional[Connection]:
        return self.db.query(Connection).filter(
            Connection.id == connection_id
        ).first()
    
    def list_connections(
        self,
        user_id: str,
        connector_type: Optional[str] = None
    ) -> List[Connection]:
        query = self.db.query(Connection).filter(
            Connection.user_id == user_id
        )
        
        if connector_type:
            query = query.filter(Connection.connector_type == connector_type)
        
        return query.all()
    
    def update_connection(
        self,
        connection_id: str,
        **kwargs
    ) -> Optional[Connection]:
        connection = self.get_connection(connection_id)
        
        if not connection:
            return None
        
        for key, value in kwargs.items():
            if hasattr(connection, key):
                setattr(connection, key, value)
        
        connection.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(connection)
        
        return connection
    
    def delete_connection(self, connection_id: str) -> bool:
        connection = self.get_connection(connection_id)
        
        if not connection:
            return False
        
        self.db.query(OAuthToken).filter(
            OAuthToken.connection_id == connection_id
        ).delete()
        
        self.db.delete(connection)
        self.db.commit()
        
        return True
    
    def store_oauth_token(
        self,
        connection_id: str,
        token_data: Dict
    ) -> OAuthToken:
        existing_token = self.db.query(OAuthToken).filter(
            OAuthToken.connection_id == connection_id
        ).first()
        
        if existing_token:
            self.db.delete(existing_token)
        
        from platform.core.oauth_manager import OAuthManager
        oauth_manager = OAuthManager(self.db)
        
        expires_at = None
        if "expires_in" in token_data:
            expires_at = oauth_manager.calculate_expiry(token_data["expires_in"])
        
        token = OAuthToken(
            id=str(uuid.uuid4()),
            connection_id=connection_id,
            access_token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            token_type=token_data.get("token_type", "Bearer"),
            expires_at=expires_at,
            scope=token_data.get("scope")
        )
        
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        
        return token
    
    def get_oauth_token(self, connection_id: str) -> Optional[OAuthToken]:
        return self.db.query(OAuthToken).filter(
            OAuthToken.connection_id == connection_id
        ).first()
