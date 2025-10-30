"""
OneDrive Connector
Generated from configuration
"""
from sdk.python.base_connector import BaseConnector
from typing import Dict, List, Optional, Any


class OnedriveConnector(BaseConnector):
    """Connect to Microsoft OneDrive to manage files and folders"""
    
    def __init__(self, connection_id: str, config: Dict):
        super().__init__(connection_id, config)
        self.connector_name = "onedrive"
        self.base_url = "https://graph.microsoft.com/v1.0"
    

    def list_files(self, top: int = None, orderby: str = None) -> Dict[str, Any]:
        """
        List files and folders in the root directory
        
        Args:

            top: Number of items to return

            orderby: Sort order (name, lastModifiedDateTime, size)

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/me/drive/root/children",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if top is not None:
            params["top"] = top
        

        
        if orderby is not None:
            params["orderby"] = orderby
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def get_file(self, itemId: str) -> Dict[str, Any]:
        """
        Get metadata for a specific file or folder
        
        Args:

            itemId: The ID of the file or folder

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/me/drive/items/{itemId}",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if itemId is not None:
            path_params["itemId"] = itemId
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def download_file(self, itemId: str) -> Dict[str, Any]:
        """
        Download the content of a file
        
        Args:

            itemId: The ID of the file to download

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/me/drive/items/{itemId}/content",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if itemId is not None:
            path_params["itemId"] = itemId
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def upload_file(self, filename: str, content: str) -> Dict[str, Any]:
        """
        Upload a new file or replace existing file
        
        Args:

            filename: Name of the file to upload

            content: File content (base64 encoded for binary files)

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "PUT",
            "path": "/me/drive/root:/{filename}:/content",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if filename is not None:
            path_params["filename"] = filename
        

        
        if content is not None:
            body["content"] = content
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def create_folder(self, name: str, folder: dict) -> Dict[str, Any]:
        """
        Create a new folder
        
        Args:

            name: Name of the folder

            folder: Folder object (empty dict)

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/me/drive/root/children",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if name is not None:
            body["name"] = name
        

        
        if folder is not None:
            body["folder"] = folder
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def delete_item(self, itemId: str) -> Dict[str, Any]:
        """
        Delete a file or folder
        
        Args:

            itemId: The ID of the file or folder to delete

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "DELETE",
            "path": "/me/drive/items/{itemId}",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if itemId is not None:
            path_params["itemId"] = itemId
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def search_files(self, query: str, top: int = None) -> Dict[str, Any]:
        """
        Search for files and folders
        
        Args:

            query: Search query

            top: Number of results to return

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "GET",
            "path": "/me/drive/root/search(q='{query}')",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if query is not None:
            path_params["query"] = query
        

        
        if top is not None:
            params["top"] = top
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def copy_item(self, itemId: str, parentReference: dict, name: str = None) -> Dict[str, Any]:
        """
        Copy a file or folder to a new location
        
        Args:

            itemId: The ID of the item to copy

            parentReference: Reference to the parent folder

            name: New name for the copied item

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/me/drive/items/{itemId}/copy",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if itemId is not None:
            path_params["itemId"] = itemId
        

        
        if parentReference is not None:
            body["parentReference"] = parentReference
        

        
        if name is not None:
            body["name"] = name
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )

