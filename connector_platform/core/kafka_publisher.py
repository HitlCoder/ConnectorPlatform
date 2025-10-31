from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class KafkaPublisher:
    """Publishes transformed data to Kafka topics by connector type"""
    
    def __init__(self, bootstrap_servers: Optional[str] = None, enabled: bool = True):
        """
        Initialize Kafka publisher
        
        Args:
            bootstrap_servers: Kafka bootstrap servers (comma-separated)
            enabled: Whether Kafka publishing is enabled
        """
        self.enabled = enabled
        self.bootstrap_servers = bootstrap_servers or 'localhost:9092'
        self.producer = None
        
        if self.enabled:
            self._initialize_producer()
    
    def _initialize_producer(self):
        """Initialize Kafka producer"""
        try:
            from kafka import KafkaProducer
            
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers.split(','),
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            logger.info(f"Kafka producer initialized with servers: {self.bootstrap_servers}")
        except ImportError:
            logger.warning("kafka-python not installed. Kafka publishing disabled.")
            self.enabled = False
            self.producer = None
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            self.enabled = False
            self.producer = None
    
    def publish(
        self,
        connector_type: str,
        data: Dict[str, Any],
        connection_id: str,
        connector_name: str,
        endpoint_name: str
    ) -> bool:
        """
        Publish transformed data to Kafka topic
        
        Args:
            connector_type: Type of connector (cloud_storage, email, marketing)
            data: Transformed data to publish
            connection_id: Connection ID
            connector_name: Name of the connector
            endpoint_name: Name of the endpoint
        
        Returns:
            True if published successfully, False otherwise
        """
        if not self.enabled or not self.producer:
            logger.debug("Kafka publishing disabled or producer not initialized")
            return False
        
        topic = self._get_topic_name(connector_type)
        
        message = {
            'connector_type': connector_type,
            'connector_name': connector_name,
            'connection_id': connection_id,
            'endpoint_name': endpoint_name,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        
        try:
            future = self.producer.send(
                topic,
                value=message,
                key=connection_id
            )
            
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"Published to Kafka topic '{topic}': "
                f"partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish to Kafka topic '{topic}': {e}")
            return False
    
    def _get_topic_name(self, connector_type: str) -> str:
        """Get Kafka topic name for connector type"""
        return f"connector-platform.{connector_type}"
    
    def flush(self):
        """Flush pending messages"""
        if self.producer:
            self.producer.flush()
    
    def close(self):
        """Close Kafka producer"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")


class MockKafkaPublisher(KafkaPublisher):
    """Mock Kafka publisher for testing and development"""
    
    def __init__(self):
        """Initialize mock publisher"""
        self.enabled = True
        self.producer = None
        self.published_messages = []
    
    def publish(
        self,
        connector_type: str,
        data: Dict[str, Any],
        connection_id: str,
        connector_name: str,
        endpoint_name: str
    ) -> bool:
        """Mock publish - stores messages in memory"""
        topic = self._get_topic_name(connector_type)
        
        message = {
            'topic': topic,
            'connector_type': connector_type,
            'connector_name': connector_name,
            'connection_id': connection_id,
            'endpoint_name': endpoint_name,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        
        self.published_messages.append(message)
        
        logger.info(
            f"[MOCK] Published to topic '{topic}': "
            f"connector={connector_name}, endpoint={endpoint_name}"
        )
        return True
    
    def get_messages(self, topic: Optional[str] = None) -> list:
        """Get published messages (for testing)"""
        if topic:
            return [m for m in self.published_messages if m['topic'] == topic]
        return self.published_messages
    
    def clear(self):
        """Clear published messages"""
        self.published_messages = []
