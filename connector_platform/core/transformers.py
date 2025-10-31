from typing import Dict, Any, List, Optional
from datetime import datetime
from .data_models import (
    CloudStorageFile, CloudStorageFileList,
    EmailMessage, EmailMessageList,
    MarketingContact, MarketingCampaign
)


class BaseTransformer:
    """Base class for all transformers"""
    
    def transform(self, data: Dict[str, Any], endpoint_name: str, connector_name: str) -> Dict[str, Any]:
        """Transform connector-specific data to common model"""
        raise NotImplementedError("Subclasses must implement transform method")


class CloudStorageTransformer(BaseTransformer):
    """Transformer for cloud storage connectors (OneDrive, Dropbox, Google Drive)"""
    
    def transform(self, data: Dict[str, Any], endpoint_name: str, connector_name: str) -> Dict[str, Any]:
        """Transform cloud storage responses to common CloudStorage model"""
        
        if endpoint_name in ['list_files', 'list_folder', 'search_files']:
            return self._transform_file_list(data, connector_name)
        elif endpoint_name in ['get_file', 'get_metadata']:
            return self._transform_single_file(data, connector_name)
        else:
            return {'raw_data': data, 'transformed': False}
    
    def _transform_file_list(self, data: Dict[str, Any], connector_name: str) -> Dict[str, Any]:
        """Transform file list response to common model"""
        
        if connector_name == 'onedrive':
            items = data.get('value', [])
            files = [self._transform_onedrive_file(item) for item in items]
            return CloudStorageFileList(
                files=files,
                total_count=len(files),
                has_more='@odata.nextLink' in data,
                next_cursor=data.get('@odata.nextLink'),
                metadata={'connector': 'onedrive', 'raw_count': len(items)}
            ).to_dict()
        
        elif connector_name == 'dropbox':
            entries = data.get('entries', [])
            files = [self._transform_dropbox_file(entry) for entry in entries]
            return CloudStorageFileList(
                files=files,
                total_count=len(files),
                has_more=data.get('has_more', False),
                next_cursor=data.get('cursor'),
                metadata={'connector': 'dropbox', 'raw_count': len(entries)}
            ).to_dict()
        
        return {'raw_data': data, 'transformed': False}
    
    def _transform_single_file(self, data: Dict[str, Any], connector_name: str) -> Dict[str, Any]:
        """Transform single file response to common model"""
        
        if connector_name == 'onedrive':
            file_obj = self._transform_onedrive_file(data)
        elif connector_name == 'dropbox':
            file_obj = self._transform_dropbox_file(data)
        else:
            return {'raw_data': data, 'transformed': False}
        
        return file_obj.to_dict()
    
    def _transform_onedrive_file(self, item: Dict[str, Any]) -> CloudStorageFile:
        """Transform OneDrive file item to common model"""
        return CloudStorageFile(
            id=item.get('id', ''),
            name=item.get('name', ''),
            path=item.get('parentReference', {}).get('path', '') + '/' + item.get('name', ''),
            type='file' if 'file' in item else 'folder',
            size=item.get('size'),
            created_at=self._parse_datetime(item.get('createdDateTime')),
            modified_at=self._parse_datetime(item.get('lastModifiedDateTime')),
            mime_type=item.get('file', {}).get('mimeType'),
            is_folder='folder' in item,
            parent_id=item.get('parentReference', {}).get('id'),
            download_url=item.get('@microsoft.graph.downloadUrl'),
            shared=item.get('shared') is not None,
            metadata={
                'web_url': item.get('webUrl'),
                'created_by': item.get('createdBy', {}).get('user', {}).get('displayName'),
                'modified_by': item.get('lastModifiedBy', {}).get('user', {}).get('displayName')
            }
        )
    
    def _transform_dropbox_file(self, entry: Dict[str, Any]) -> CloudStorageFile:
        """Transform Dropbox file entry to common model"""
        tag = entry.get('.tag', 'file')
        return CloudStorageFile(
            id=entry.get('id', entry.get('path_display', '')),
            name=entry.get('name', ''),
            path=entry.get('path_display', ''),
            type=tag,
            size=entry.get('size'),
            created_at=None,
            modified_at=self._parse_datetime(entry.get('client_modified') or entry.get('server_modified')),
            mime_type=None,
            is_folder=tag == 'folder',
            parent_id=entry.get('path_lower', '').rsplit('/', 1)[0] if '/' in entry.get('path_lower', '') else None,
            download_url=None,
            shared=entry.get('sharing_info') is not None,
            metadata={
                'rev': entry.get('rev'),
                'content_hash': entry.get('content_hash')
            }
        )
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse ISO datetime string"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None


class EmailTransformer(BaseTransformer):
    """Transformer for email connectors (Gmail, Outlook)"""
    
    def transform(self, data: Dict[str, Any], endpoint_name: str, connector_name: str) -> Dict[str, Any]:
        """Transform email responses to common Email model"""
        
        if endpoint_name == 'list_messages':
            return self._transform_message_list(data, connector_name)
        elif endpoint_name == 'get_message':
            return self._transform_single_message(data, connector_name)
        else:
            return {'raw_data': data, 'transformed': False}
    
    def _transform_message_list(self, data: Dict[str, Any], connector_name: str) -> Dict[str, Any]:
        """Transform message list response to common model"""
        
        if connector_name == 'gmail':
            messages_data = data.get('messages', [])
            messages = []
            
            for msg in messages_data:
                messages.append(EmailMessage(
                    id=msg.get('id', ''),
                    thread_id=msg.get('threadId'),
                    subject='',
                    from_address='',
                    to_addresses=[],
                    snippet='',
                    metadata={'gmail_id': msg.get('id')}
                ))
            
            return EmailMessageList(
                messages=messages,
                total_count=data.get('resultSizeEstimate', len(messages)),
                has_more='nextPageToken' in data,
                next_page_token=data.get('nextPageToken'),
                metadata={'connector': 'gmail'}
            ).to_dict()
        
        return {'raw_data': data, 'transformed': False}
    
    def _transform_single_message(self, data: Dict[str, Any], connector_name: str) -> Dict[str, Any]:
        """Transform single message response to common model"""
        
        if connector_name == 'gmail':
            return self._transform_gmail_message(data).to_dict()
        
        return {'raw_data': data, 'transformed': False}
    
    def _transform_gmail_message(self, msg: Dict[str, Any]) -> EmailMessage:
        """Transform Gmail message to common model"""
        headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
        
        return EmailMessage(
            id=msg.get('id', ''),
            thread_id=msg.get('threadId'),
            subject=headers.get('Subject', ''),
            from_address=headers.get('From', ''),
            to_addresses=[headers.get('To', '')],
            cc_addresses=[headers.get('Cc')] if headers.get('Cc') else None,
            snippet=msg.get('snippet'),
            received_at=self._parse_gmail_date(headers.get('Date')),
            labels=msg.get('labelIds', []),
            is_read='UNREAD' not in msg.get('labelIds', []),
            is_starred='STARRED' in msg.get('labelIds', []),
            metadata={
                'gmail_id': msg.get('id'),
                'history_id': msg.get('historyId'),
                'internal_date': msg.get('internalDate')
            }
        )
    
    def _parse_gmail_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse Gmail date header"""
        if not date_str:
            return None
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except (ValueError, TypeError):
            return None


class MarketingTransformer(BaseTransformer):
    """Transformer for marketing connectors (Marketo, Klaviyo, Mailchimp)"""
    
    def transform(self, data: Dict[str, Any], endpoint_name: str, connector_name: str) -> Dict[str, Any]:
        """Transform marketing platform responses to common model"""
        
        return {'raw_data': data, 'transformed': False, 'note': 'Marketing transformer placeholder'}


class TransformerFactory:
    """Factory to get appropriate transformer based on connector type"""
    
    _transformers = {
        'cloud_storage': CloudStorageTransformer(),
        'email': EmailTransformer(),
        'marketing': MarketingTransformer()
    }
    
    @classmethod
    def get_transformer(cls, connector_type: str) -> Optional[BaseTransformer]:
        """Get transformer for given connector type"""
        return cls._transformers.get(connector_type)
    
    @classmethod
    def register_transformer(cls, connector_type: str, transformer: BaseTransformer):
        """Register a new transformer for a connector type"""
        cls._transformers[connector_type] = transformer
