"""
Gmail Connector
Generated from configuration
"""
from sdk.python.base_connector import BaseConnector
from typing import Dict, List, Optional, Any


class GmailConnector(BaseConnector):
    """Connect to Gmail to send, read, and manage emails"""
    
    def __init__(self, connection_id: str, config: Dict):
        super().__init__(connection_id, config)
        self.connector_name = "gmail"
        self.base_url = "https://gmail.googleapis.com"
    

    def list_messages(self, maxResults: int = None, q: str = None) -> Dict[str, Any]:
        """
        List messages in the user's mailbox
        
        Args:

            maxResults: Maximum number of messages to return

            q: Query string to filter messages

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/gmail/v1/users/me/messages",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if maxResults is not None:
            params["maxResults"] = maxResults
        

        
        if q is not None:
            params["q"] = q
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def get_message(self, messageId: str, format: str = None) -> Dict[str, Any]:
        """
        Get a specific message by ID
        
        Args:

            messageId: The ID of the message to retrieve

            format: Format of the message (full, metadata, minimal, raw)

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/gmail/v1/users/me/messages/{messageId}",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if messageId is not None:
            path_params["messageId"] = messageId
        

        
        if format is not None:
            params["format"] = format
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def send_message(self, raw: str) -> Dict[str, Any]:
        """
        Send an email message
        
        Args:

            raw: Base64-encoded email message in RFC 2822 format

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/gmail/v1/users/me/messages/send",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if raw is not None:
            body["raw"] = raw
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def delete_message(self, messageId: str) -> Dict[str, Any]:
        """
        Delete a message
        
        Args:

            messageId: The ID of the message to delete

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "DELETE",
            "path": "/gmail/v1/users/me/messages/{messageId}",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if messageId is not None:
            path_params["messageId"] = messageId
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def list_labels(self) -> Dict[str, Any]:
        """
        List all labels in the user's mailbox
        
        Args:

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/gmail/v1/users/me/labels",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def modify_message(self, messageId: str, addLabelIds: list = None, removeLabelIds: list = None) -> Dict[str, Any]:
        """
        Modify the labels on a message
        
        Args:

            messageId: The ID of the message to modify

            addLabelIds: List of label IDs to add

            removeLabelIds: List of label IDs to remove

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/gmail/v1/users/me/messages/{messageId}/modify",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if messageId is not None:
            path_params["messageId"] = messageId
        

        
        if addLabelIds is not None:
            body["addLabelIds"] = addLabelIds
        

        
        if removeLabelIds is not None:
            body["removeLabelIds"] = removeLabelIds
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )

