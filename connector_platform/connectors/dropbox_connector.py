"""
Dropbox Connector
Generated from configuration
"""
from sdk.python.base_connector import BaseConnector
from typing import Dict, List, Optional, Any


class DropboxConnector(BaseConnector):
    """Connect to Dropbox to manage files and folders"""
    
    def __init__(self, connection_id: str, config: Dict):
        super().__init__(connection_id, config)
        self.connector_name = "dropbox"
        self.base_url = "https://api.dropboxapi.com/2"
    

    def list_folder(self, path: str, recursive: bool = None, limit: int = None) -> Dict[str, Any]:
        """
        List contents of a folder
        
        Args:

            path: Path to the folder (empty string for root)

            recursive: Whether to list all subfolders recursively

            limit: Maximum number of results

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/list_folder",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        if recursive is not None:
            body["recursive"] = recursive
        

        
        if limit is not None:
            body["limit"] = limit
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def get_metadata(self, path: str) -> Dict[str, Any]:
        """
        Get metadata for a file or folder
        
        Args:

            path: Path to the file or folder

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/get_metadata",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def download_file(self, path: str) -> Dict[str, Any]:
        """
        Download a file
        
        Args:

            path: Path to the file to download

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/download",
            "headers": {'Dropbox-API-Arg': '{"path": "{path}"}'}
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def upload_file(self, path: str, content: str) -> Dict[str, Any]:
        """
        Upload a file
        
        Args:

            path: Path where the file should be saved

            content: File content

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/upload",
            "headers": {'Content-Type': 'application/octet-stream', 'Dropbox-API-Arg': '{"path": "{path}", "mode": "add", "autorename": true}'}
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        if content is not None:
            body["content"] = content
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def create_folder(self, path: str, autorename: bool = None) -> Dict[str, Any]:
        """
        Create a new folder
        
        Args:

            path: Path for the new folder

            autorename: Auto-rename if folder exists

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/create_folder_v2",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        if autorename is not None:
            body["autorename"] = autorename
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def delete_item(self, path: str) -> Dict[str, Any]:
        """
        Delete a file or folder
        
        Args:

            path: Path to the file or folder to delete

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/delete_v2",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def move_item(self, from_path: str, to_path: str, autorename: bool = None) -> Dict[str, Any]:
        """
        Move a file or folder
        
        Args:

            from_path: Source path

            to_path: Destination path

            autorename: Auto-rename if item exists at destination

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/move_v2",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if from_path is not None:
            body["from_path"] = from_path
        

        
        if to_path is not None:
            body["to_path"] = to_path
        

        
        if autorename is not None:
            body["autorename"] = autorename
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def search_files(self, query: str, options: dict = None) -> Dict[str, Any]:
        """
        Search for files and folders
        
        Args:

            query: Search query

            options: Search options

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/files/search_v2",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if query is not None:
            body["query"] = query
        

        
        if options is not None:
            body["options"] = options
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )


    def create_shared_link(self, path: str, settings: dict = None) -> Dict[str, Any]:
        """
        Create a shared link for a file or folder
        
        Args:

            path: Path to the file or folder

            settings: Sharing settings

        
        Returns:
            Dict containing the API response
        """
        endpoint_config = {
            "method": "POST",
            "path": "/sharing/create_shared_link_with_settings",
            "headers": 
        }
        
        params = {}
        body = {}
        path_params = {}
        

        
        if path is not None:
            body["path"] = path
        

        
        if settings is not None:
            body["settings"] = settings
        

        
        return self.execute_request(
            endpoint_config=endpoint_config,
            params=params if params else None,
            body=body if body else None,
            path_params=path_params if path_params else None
        )

