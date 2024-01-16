# kafka_consumer/__init__.py
import logging

from message_consumer.kafka_consumer import KafkaConsumer
from constant import KAFKA_BOOTSTRAP_SERVERS,KAFKA_MIGRATION_TOPIC,KAFKA_GROUP_ID
import signal

from message_consumer.callbacks import custom_callback
logger = logging.getLogger(__name__)


# Define Kafka consumer configuration
kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
kafka_group_id = KAFKA_GROUP_ID
kafka_topics = KAFKA_MIGRATION_TOPIC

# Start Kafka consumer thread
kafka_thread = KafkaConsumer(
    bootstrap_servers=kafka_bootstrap_servers,
    group_id=kafka_group_id,
    topics=kafka_topics
)

# Set the callback dynamically
kafka_thread.process_message = custom_callback

# Start the consumer thread
kafka_thread.start()


# Handle graceful shutdown on keyboard interrupt
def shutdown_handler(signum, frame):
    if kafka_thread.is_alive():
        logger.info("Shutting down Kafka consumer thread...")
        kafka_thread.stop()
        kafka_thread.join(timeout=30)  # Allow up to 30 seconds for the thread to join
        if kafka_thread.is_alive():
            logger.warning("Kafka consumer thread did not stop gracefully.")
    exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
