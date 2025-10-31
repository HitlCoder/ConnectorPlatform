"""
Example: Data Transformation and Kafka Publishing

This example demonstrates how the Connector Platform automatically:
1. Transforms API responses to common data models
2. Publishes transformed data to Kafka topics by connector type
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def example_onedrive_list_files():
    """
    Example: List files from OneDrive
    
    The response will be transformed to CloudStorageFileList format
    and published to Kafka topic: connector-platform.cloud_storage
    """
    
    # Step 1: Execute API request through the proxy
    response = requests.post(
        f"{BASE_URL}/api/v1/proxy/execute",
        json={
            "connection_id": "your-onedrive-connection-id",
            "endpoint_config": {
                "name": "list_files",
                "display_name": "List Files",
                "method": "GET",
                "path": "/me/drive/root/children",
                "response_type": "json"
            },
            "params": {
                "top": 10  # Limit to 10 files
            }
        }
    )
    
    result = response.json()
    
    print("=== OneDrive List Files ===\n")
    
    # Original raw response from OneDrive
    print("Raw OneDrive Response:")
    print(json.dumps(result.get('data'), indent=2)[:500] + "...\n")
    
    # Transformed data in common CloudStorageFileList format
    print("Transformed to Common Format (CloudStorageFileList):")
    transformed = result.get('transformed_data', {})
    print(json.dumps(transformed, indent=2)[:500] + "...\n")
    
    # Kafka publishing status
    print(f"Published to Kafka: {result.get('published_to_kafka', False)}")
    print(f"Connector Type: {result.get('connector_type', 'N/A')}")
    print(f"Kafka Topic: connector-platform.{result.get('connector_type', 'N/A')}\n")
    
    # Access transformed files
    if 'files' in transformed:
        print(f"Total Files: {transformed.get('total_count', 0)}")
        print(f"Has More: {transformed.get('has_more', False)}")
        print("\nFirst File in Common Format:")
        if transformed['files']:
            first_file = transformed['files'][0]
            print(f"  ID: {first_file.get('id')}")
            print(f"  Name: {first_file.get('name')}")
            print(f"  Path: {first_file.get('path')}")
            print(f"  Type: {first_file.get('type')}")
            print(f"  Size: {first_file.get('size')} bytes")
            print(f"  Modified: {first_file.get('modified_at')}")
            print(f"  Is Folder: {first_file.get('is_folder')}")


def example_dropbox_list_folder():
    """
    Example: List folder contents from Dropbox
    
    The response will be transformed to the same CloudStorageFileList format
    as OneDrive, allowing unified processing!
    """
    
    response = requests.post(
        f"{BASE_URL}/api/v1/proxy/execute",
        json={
            "connection_id": "your-dropbox-connection-id",
            "endpoint_config": {
                "name": "list_folder",
                "display_name": "List Folder",
                "method": "POST",
                "path": "/files/list_folder",
                "response_type": "json"
            },
            "params": {},
            "body": {
                "path": "",  # Root folder
                "limit": 10
            }
        }
    )
    
    result = response.json()
    
    print("=== Dropbox List Folder ===\n")
    
    # Both OneDrive and Dropbox now return the same format!
    transformed = result.get('transformed_data', {})
    
    print("Transformed to Common Format (CloudStorageFileList):")
    print(f"Total Files: {transformed.get('total_count', 0)}")
    print(f"Connector: {transformed.get('metadata', {}).get('connector')}")
    
    # The structure is identical to OneDrive transformation
    # This allows you to process files from any cloud storage provider
    # using the same code!


def example_gmail_list_messages():
    """
    Example: List email messages from Gmail
    
    The response will be transformed to EmailMessageList format
    and published to Kafka topic: connector-platform.email
    """
    
    response = requests.post(
        f"{BASE_URL}/api/v1/proxy/execute",
        json={
            "connection_id": "your-gmail-connection-id",
            "endpoint_config": {
                "name": "list_messages",
                "display_name": "List Messages",
                "method": "GET",
                "path": "/gmail/v1/users/me/messages",
                "response_type": "json"
            },
            "params": {
                "maxResults": 10,
                "q": "is:unread"  # Only unread messages
            }
        }
    )
    
    result = response.json()
    
    print("=== Gmail List Messages ===\n")
    
    # Original Gmail response
    print("Raw Gmail Response:")
    print(json.dumps(result.get('data'), indent=2)[:300] + "...\n")
    
    # Transformed to EmailMessageList
    transformed = result.get('transformed_data', {})
    
    print("Transformed to Common Format (EmailMessageList):")
    print(json.dumps(transformed, indent=2)[:500] + "...\n")
    
    print(f"Kafka Topic: connector-platform.email")


def compare_transformations():
    """
    Compare raw vs transformed data side by side
    """
    
    print("=== Transformation Comparison ===\n")
    
    print("OneDrive Raw Response Structure:")
    print("""
    {
      "value": [
        {
          "id": "01BYE5...",
          "name": "file.pdf",
          "size": 1024,
          "lastModifiedDateTime": "2025-01-15T10:30:00Z",
          "file": { "mimeType": "application/pdf" },
          ...
        }
      ]
    }
    """)
    
    print("\nDropbox Raw Response Structure:")
    print("""
    {
      "entries": [
        {
          ".tag": "file",
          "name": "file.pdf",
          "path_display": "/file.pdf",
          "size": 1024,
          "server_modified": "2025-01-15T10:30:00Z",
          ...
        }
      ]
    }
    """)
    
    print("\n✨ Both Transform To Same Common Format:")
    print("""
    {
      "files": [
        {
          "id": "...",
          "name": "file.pdf",
          "path": "/file.pdf",
          "type": "file",
          "size": 1024,
          "modified_at": "2025-01-15T10:30:00+00:00",
          "is_folder": false,
          ...
        }
      ],
      "total_count": 1,
      "has_more": false
    }
    """)
    
    print("\n🎯 Benefits:")
    print("  ✓ Write once, works with all cloud storage providers")
    print("  ✓ Consume from single Kafka topic for all providers")
    print("  ✓ Build analytics across multiple platforms")
    print("  ✓ Easy migration between providers")


def kafka_message_example():
    """
    Show what messages look like in Kafka
    """
    
    print("=== Kafka Message Example ===\n")
    
    print("Topic: connector-platform.cloud_storage")
    print("Key: connection-id-123\n")
    
    print("Message Value:")
    example_message = {
        "connector_type": "cloud_storage",
        "connector_name": "onedrive",
        "connection_id": "conn-123",
        "endpoint_name": "list_files",
        "timestamp": "2025-01-15T10:30:00Z",
        "data": {
            "files": [
                {
                    "id": "file-id-123",
                    "name": "quarterly-report.pdf",
                    "path": "/Documents/quarterly-report.pdf",
                    "type": "file",
                    "size": 2048000,
                    "created_at": "2025-01-01T12:00:00+00:00",
                    "modified_at": "2025-01-15T10:30:00+00:00",
                    "mime_type": "application/pdf",
                    "is_folder": False,
                    "parent_id": "folder-id-456",
                    "download_url": "https://...",
                    "shared": False,
                    "metadata": {
                        "web_url": "https://...",
                        "created_by": "John Doe",
                        "modified_by": "Jane Smith"
                    }
                }
            ],
            "total_count": 1,
            "has_more": False,
            "next_cursor": None,
            "metadata": {
                "connector": "onedrive",
                "raw_count": 1
            }
        }
    }
    
    print(json.dumps(example_message, indent=2))


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Connector Platform - Data Transformation Examples")
    print("="*60 + "\n")
    
    # Compare raw vs transformed structures
    compare_transformations()
    
    print("\n" + "="*60 + "\n")
    
    # Show Kafka message format
    kafka_message_example()
    
    print("\n" + "="*60)
    print("\n💡 To run actual API calls:")
    print("   1. Create connections for OneDrive, Dropbox, or Gmail")
    print("   2. Complete OAuth authorization")
    print("   3. Replace connection IDs in the examples above")
    print("   4. Run: python examples/transformation_example.py")
    print("\n" + "="*60 + "\n")
