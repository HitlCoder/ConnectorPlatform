"""
Unit tests for data transformation and Kafka integration

Run with: python tests/test_transformation.py
"""
import sys
sys.path.insert(0, '.')

from connector_platform.core.data_models import CloudStorageFile, CloudStorageFileList
from connector_platform.core.transformers import CloudStorageTransformer, EmailTransformer, TransformerFactory
from connector_platform.core.kafka_publisher import MockKafkaPublisher
from datetime import datetime

def test_cloud_storage_transformer():
    """Test OneDrive transformation"""
    print("Testing CloudStorageTransformer with OneDrive data...")
    
    onedrive_response = {
        "value": [
            {
                "id": "01BYE5RZ6QN3VZQIPQZQBL2QZAYVQK3IOV",
                "name": "test.pdf",
                "size": 1024000,
                "lastModifiedDateTime": "2025-01-15T10:30:00Z",
                "createdDateTime": "2025-01-01T12:00:00Z",
                "file": {"mimeType": "application/pdf"},
                "parentReference": {
                    "id": "parent-id",
                    "path": "/drive/root:/Documents"
                },
                "webUrl": "https://onedrive.live.com/..."
            },
            {
                "id": "folder-id-123",
                "name": "My Folder",
                "folder": {"childCount": 5},
                "lastModifiedDateTime": "2025-01-10T08:00:00Z",
                "createdDateTime": "2024-12-01T10:00:00Z",
                "parentReference": {
                    "id": "root-id",
                    "path": "/drive/root:"
                }
            }
        ],
        "@odata.nextLink": "https://graph.microsoft.com/v1.0/..."
    }
    
    transformer = CloudStorageTransformer()
    result = transformer.transform(onedrive_response, "list_files", "onedrive")
    
    assert "files" in result, "Missing 'files' key"
    assert result["total_count"] == 2, f"Expected 2 files, got {result['total_count']}"
    assert result["has_more"] == True, "Should have more results"
    
    file1 = result["files"][0]
    assert file1["name"] == "test.pdf"
    assert file1["size"] == 1024000
    assert file1["type"] == "file"
    assert file1["is_folder"] == False
    
    folder = result["files"][1]
    assert folder["name"] == "My Folder"
    assert folder["type"] == "folder"
    assert folder["is_folder"] == True
    
    print("✓ OneDrive transformation successful")
    return True


def test_dropbox_transformer():
    """Test Dropbox transformation"""
    print("\nTesting CloudStorageTransformer with Dropbox data...")
    
    dropbox_response = {
        "entries": [
            {
                ".tag": "file",
                "name": "report.docx",
                "path_display": "/Work/report.docx",
                "id": "id:dropbox-file-id",
                "size": 524288,
                "server_modified": "2025-01-20T14:00:00Z",
                "client_modified": "2025-01-20T13:55:00Z"
            }
        ],
        "has_more": False
    }
    
    transformer = CloudStorageTransformer()
    result = transformer.transform(dropbox_response, "list_folder", "dropbox")
    
    assert "files" in result
    assert result["total_count"] == 1
    assert result["has_more"] == False
    
    print("✓ Dropbox transformation successful")
    return True


def test_transformer_factory():
    """Test TransformerFactory"""
    print("\nTesting TransformerFactory...")
    
    cloud_transformer = TransformerFactory.get_transformer("cloud_storage")
    email_transformer = TransformerFactory.get_transformer("email")
    unknown_transformer = TransformerFactory.get_transformer("unknown_type")
    
    assert cloud_transformer is not None
    assert email_transformer is not None
    assert unknown_transformer is not None
    
    print("✓ TransformerFactory working correctly")
    return True


def test_kafka_publisher():
    """Test MockKafkaPublisher"""
    print("\nTesting MockKafkaPublisher...")
    
    publisher = MockKafkaPublisher()
    
    test_data = {
        "files": [{"id": "1", "name": "test.txt"}],
        "total_count": 1
    }
    
    publisher.publish(
        connector_type="cloud_storage",
        data=test_data,
        connection_id="connection-123",
        connector_name="onedrive",
        endpoint_name="list_files"
    )
    
    messages = publisher.get_messages()
    assert len(messages) == 1
    
    msg = messages[0]
    assert msg["topic"] == "connector-platform.cloud_storage"
    assert msg["connector_type"] == "cloud_storage"
    
    publisher.clear()
    assert len(publisher.get_messages()) == 0
    
    print("✓ MockKafkaPublisher working correctly")
    return True


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Running Transformation & Kafka Integration Tests")
    print("="*60)
    
    try:
        test_cloud_storage_transformer()
        test_dropbox_transformer()
        test_transformer_factory()
        test_kafka_publisher()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
