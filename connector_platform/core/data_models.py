from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class CloudStorageFile:
    """Common data model for cloud storage files across providers"""
    id: str
    name: str
    path: str
    type: str
    size: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    mime_type: Optional[str] = None
    is_folder: bool = False
    parent_id: Optional[str] = None
    download_url: Optional[str] = None
    shared: bool = False
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.modified_at:
            data['modified_at'] = self.modified_at.isoformat()
        return data


@dataclass
class CloudStorageFileList:
    """Common data model for list of cloud storage files"""
    files: List[CloudStorageFile]
    total_count: int
    has_more: bool = False
    next_cursor: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'files': [f.to_dict() for f in self.files],
            'total_count': self.total_count,
            'has_more': self.has_more,
            'next_cursor': self.next_cursor,
            'metadata': self.metadata
        }


@dataclass
class EmailMessage:
    """Common data model for email messages"""
    id: str
    thread_id: Optional[str]
    subject: str
    from_address: str
    to_addresses: List[str]
    cc_addresses: Optional[List[str]] = None
    bcc_addresses: Optional[List[str]] = None
    body: Optional[str] = None
    html_body: Optional[str] = None
    snippet: Optional[str] = None
    received_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    labels: Optional[List[str]] = None
    is_read: bool = False
    is_starred: bool = False
    has_attachments: bool = False
    attachments: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.received_at:
            data['received_at'] = self.received_at.isoformat()
        if self.sent_at:
            data['sent_at'] = self.sent_at.isoformat()
        return data


@dataclass
class EmailMessageList:
    """Common data model for list of email messages"""
    messages: List[EmailMessage]
    total_count: int
    has_more: bool = False
    next_page_token: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'messages': [m.to_dict() for m in self.messages],
            'total_count': self.total_count,
            'has_more': self.has_more,
            'next_page_token': self.next_page_token,
            'metadata': self.metadata
        }


@dataclass
class MarketingContact:
    """Common data model for marketing contacts"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    tags: Optional[List[str]] = None
    lists: Optional[List[str]] = None
    subscribed: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    custom_fields: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            data['updated_at'] = self.updated_at.isoformat()
        return data


@dataclass
class MarketingCampaign:
    """Common data model for marketing campaigns"""
    id: str
    name: str
    type: str
    status: str
    subject: Optional[str] = None
    from_name: Optional[str] = None
    from_email: Optional[str] = None
    recipients_count: int = 0
    sent_count: int = 0
    opened_count: int = 0
    clicked_count: int = 0
    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.sent_at:
            data['sent_at'] = self.sent_at.isoformat()
        return data
