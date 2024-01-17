from django.core.management import BaseCommand

from constant import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, KAFKA_MIGRATION_TOPIC
from message_consumer.callbacks import custom_callback
from message_consumer.kafka_consumer import KafkaConsumer


class Command(BaseCommand):
    help = 'Consume messages from Kafka topic'

    def handle(self, *args, **options):
        # Kafka configuration
        kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        kafka_group_id = KAFKA_GROUP_ID
        kafka_topics = KAFKA_MIGRATION_TOPIC

        # Start Kafka consumer in a separate thread
        kafka_consumer_thread = KafkaConsumer(
            bootstrap_servers=kafka_bootstrap_servers,
            group_id=kafka_group_id,
            topics=kafka_topics
        )
        kafka_consumer_thread.process_message = custom_callback
        kafka_consumer_thread.start()

        try:
            # Keep the main thread alive to handle interrupts
            kafka_consumer_thread.join()
        except KeyboardInterrupt:
            # Stop the Kafka consumer thread if interrupted
            kafka_consumer_thread.stop()
            kafka_consumer_thread.join()
