import threading
import asyncio
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from message_consumer import kafka_consumer
from message_consumer.kafka_consumer import KafkaConsumer  # Adjust the import path
from constant import KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID, KAFKA_MIGRATION_TOPIC


def start_kafka_consumer():
    # Initialize and run the Kafka consumer
    kafka_consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID
    )
    asyncio.run(kafka_consumer.consume_message(topic=KAFKA_MIGRATION_TOPIC))


class MessageConsumerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message_consumer'

    def ready(self):
        # Start the Kafka consumer in a separate thread
        kafka_consumer_thread = threading.Thread(target=start_kafka_consumer)
        kafka_consumer_thread.start()

    # Stop the Kafka consumer when Django is shutting down
    @receiver(post_migrate)
    def on_shutdown(sender, **kwargs):
        kafka_consumer.stop()
