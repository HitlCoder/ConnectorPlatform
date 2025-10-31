# Data Transformation and Kafka Publishing Guide

## Overview

The Connector Platform now includes automatic data transformation and Kafka publishing capabilities. API responses from different connectors of the same type are transformed into common data models and published to Kafka topics organized by connector type.

## Architecture

### Connector Types

Connectors are classified into types based on their functionality:

- **`cloud_storage`**: File storage services (OneDrive, Dropbox, Google Drive)
- **`email`**: Email services (Gmail, Outlook)
- **`marketing`**: Marketing platforms (Marketo, Klaviyo, Mailchimp)

Each connector type has its own:
- Common data model
- Transformer class
- Dedicated Kafka topic

### Kafka Topics

Messages are published to topics based on connector type:

```
connector-platform.cloud_storage   # For OneDrive, Dropbox, etc.
connector-platform.email           # For Gmail, Outlook, etc.
connector-platform.marketing       # For Marketo, Klaviyo, etc.
```

## Common Data Models

### Cloud Storage

#### CloudStorageFile

```python
{
    "id": "unique-file-id",
    "name": "document.pdf",
    "path": "/folder/document.pdf",
    "type": "file",  # or "folder"
    "size": 1024000,  # bytes
    "created_at": "2025-01-01T12:00:00Z",
    "modified_at": "2025-01-15T14:30:00Z",
    "mime_type": "application/pdf",
    "is_folder": false,
    "parent_id": "parent-folder-id",
    "download_url": "https://...",
    "shared": false,
    "metadata": {}
}
```

#### CloudStorageFileList

```python
{
    "files": [...],  # List of CloudStorageFile objects
    "total_count": 42,
    "has_more": true,
    "next_cursor": "cursor-token",
    "metadata": {
        "connector": "onedrive",
        "raw_count": 42
    }
}
```

### Email

#### EmailMessage

```python
{
    "id": "message-id",
    "thread_id": "thread-id",
    "subject": "Meeting Tomorrow",
    "from_address": "sender@example.com",
    "to_addresses": ["recipient@example.com"],
    "cc_addresses": [],
    "body": "Full message body...",
    "snippet": "Message preview...",
    "received_at": "2025-01-01T10:00:00Z",
    "labels": ["INBOX", "IMPORTANT"],
    "is_read": false,
    "is_starred": true,
    "has_attachments": false,
    "metadata": {}
}
```

### Marketing

Marketing data models (MarketingContact, MarketingCampaign) are available for future implementation.

## Transformation Flow

When an API request is executed:

1. **API Call**: External API is called (e.g., OneDrive list files)
2. **Raw Response**: Original response is received from the external service
3. **Transformation**: Response is transformed to common data model based on connector type
4. **Kafka Publishing**: Transformed data is published to the appropriate Kafka topic
5. **Response**: Both raw and transformed data are returned to the client

### Example Flow

```
User Request
    ↓
API Proxy → OneDrive API
    ↓
Raw Response: {"value": [...]}  # OneDrive format
    ↓
Transformer → CloudStorageFileList
    ↓
Transformed: {"files": [...], "total_count": 10}  # Common format
    ↓
Kafka Topic: connector-platform.cloud_storage
    ↓
Response to User (includes both raw and transformed data)
```

## Configuration

### Connector Configuration

Add the `type` field to your connector YAML file:

```yaml
name: onedrive
display_name: OneDrive
type: cloud_storage  # Define connector type
version: 1.0.0
base_url: https://graph.microsoft.com/v1.0
# ... rest of configuration
```

### Environment Variables

```bash
# Kafka Configuration
KAFKA_ENABLED=true  # Set to "true" to enable real Kafka, "false" for mock
KAFKA_BOOTSTRAP_SERVERS=localhost:9092  # Comma-separated list of Kafka brokers
```

### Development Mode (Default)

By default, the platform uses `MockKafkaPublisher` which:
- Stores messages in memory
- Logs publishing events
- Does not require a running Kafka cluster
- Perfect for development and testing

### Production Mode

To enable real Kafka publishing:

```bash
export KAFKA_ENABLED=true
export KAFKA_BOOTSTRAP_SERVERS=kafka1.example.com:9092,kafka2.example.com:9092
```

## API Response Format

When transformations are enabled, API responses include additional fields:

```json
{
    "success": true,
    "status_code": 200,
    "data": {
        // Original raw response from external API
    },
    "transformed_data": {
        // Transformed data in common format
    },
    "connector_type": "cloud_storage",
    "published_to_kafka": true,
    "headers": {}
}
```

## Creating Custom Transformers

### 1. Define Your Data Model

```python
# connector_platform/core/data_models.py
from dataclasses import dataclass

@dataclass
class MyCustomModel:
    id: str
    name: str
    # ... other fields
    
    def to_dict(self):
        return asdict(self)
```

### 2. Create a Transformer

```python
# connector_platform/core/transformers.py
class MyCustomTransformer(BaseTransformer):
    def transform(self, data: Dict, endpoint_name: str, connector_name: str):
        # Transform logic here
        if endpoint_name == 'list_items':
            return self._transform_list(data, connector_name)
        return {'raw_data': data, 'transformed': False}
    
    def _transform_list(self, data: Dict, connector_name: str):
        # Specific transformation logic
        items = data.get('items', [])
        transformed_items = [
            MyCustomModel(
                id=item['id'],
                name=item['name']
            ) for item in items
        ]
        return {'items': [i.to_dict() for i in transformed_items]}
```

### 3. Register the Transformer

```python
# In transformers.py
TransformerFactory.register_transformer('my_type', MyCustomTransformer())
```

### 4. Update Connector Config

```yaml
name: my_connector
type: my_type  # Use your custom type
```

## Transformer Implementation Details

### CloudStorageTransformer

Handles transformations for:
- **OneDrive**: `list_files`, `get_file`, `search_files`
- **Dropbox**: `list_folder`, `get_metadata`, `search_files`

Normalizes differences like:
- Date format variations
- Folder vs file detection
- Path structures
- Metadata fields

### EmailTransformer

Handles transformations for:
- **Gmail**: `list_messages`, `get_message`

Normalizes:
- Header parsing
- Label/folder systems
- Date formats
- Attachment handling

## Kafka Message Format

Messages published to Kafka include metadata and transformed data:

```json
{
    "connector_type": "cloud_storage",
    "connector_name": "onedrive",
    "connection_id": "conn-123",
    "endpoint_name": "list_files",
    "timestamp": "2025-01-15T10:30:00Z",
    "data": {
        // Transformed data in common format
    }
}
```

### Message Key

Messages are keyed by `connection_id` to ensure:
- Ordered processing per connection
- Partitioning by connection
- Easy filtering and routing

## Use Cases

### 1. Unified Analytics

Consume data from `connector-platform.cloud_storage` to analyze file usage across OneDrive, Dropbox, and Google Drive in a consistent format.

### 2. Cross-Platform Integrations

Build integrations that work with multiple cloud storage providers without knowing their specific APIs.

### 3. Event-Driven Workflows

Trigger workflows based on Kafka events when files are created, modified, or deleted across any platform.

### 4. Data Warehousing

Stream transformed data to data warehouses with consistent schemas regardless of source.

## Testing

### View Mock Kafka Messages

In development mode (default), you can inspect published messages:

```python
from connector_platform.api.main import kafka_publisher

# Get all messages
messages = kafka_publisher.get_messages()

# Get messages for specific topic
cloud_storage_messages = kafka_publisher.get_messages(
    'connector-platform.cloud_storage'
)

# Clear messages
kafka_publisher.clear()
```

### Test Transformation

```bash
# Make an API request
curl -X POST http://localhost:8000/api/v1/proxy/execute \
  -H "Content-Type: application/json" \
  -d '{
    "connection_id": "your-connection-id",
    "endpoint_config": {
      "name": "list_files",
      "method": "GET",
      "path": "/me/drive/root/children"
    },
    "params": {"top": 10}
  }'
```

The response will include:
- `data`: Raw OneDrive response
- `transformed_data`: Common CloudStorageFileList format
- `published_to_kafka`: Whether it was published

## Monitoring

### Logs

The platform logs transformation and publishing events:

```
INFO: Transformed onedrive.list_files to cloud_storage format
INFO: Published onedrive.list_files to Kafka topic: connector-platform.cloud_storage
```

### Errors

Transformation errors are logged and included in the response:

```json
{
    "success": true,
    "data": {...},
    "transformation_error": "Error message here"
}
```

## Best Practices

1. **Test Transformations**: Always test transformations with real API responses
2. **Handle Missing Fields**: Use `.get()` for optional fields with defaults
3. **Preserve Raw Data**: Always include raw data for debugging
4. **Log Transformations**: Log transformation success/failure for monitoring
5. **Version Data Models**: Add version fields to data models for schema evolution

## Troubleshooting

### Kafka Not Publishing

Check:
1. `KAFKA_ENABLED` environment variable is set to `"true"`
2. Kafka brokers are accessible
3. `kafka-python` package is installed
4. Check logs for connection errors

### Transformation Not Working

Check:
1. Connector has `type` field in YAML config
2. Transformer is registered in `TransformerFactory`
3. Endpoint name matches transformer logic
4. Check logs for transformation errors

### Data Model Mismatch

If the transformed data doesn't match expected format:
1. Check the transformer implementation for that connector
2. Verify the raw response structure
3. Add custom transformation logic if needed

## Future Enhancements

- Schema registry integration for Kafka messages
- Configurable transformation rules via YAML
- Support for custom Python transformation scripts
- Real-time transformation validation
- Transformation metrics and monitoring dashboard
