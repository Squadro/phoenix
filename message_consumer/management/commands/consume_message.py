from django.core.management import BaseCommand

from constant import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, KAFKA_MIGRATION_TOPIC
from message_consumer.callbacks import custom_callback
from message_consumer.kafka_consumer import KafkaConsumer


class Command(BaseCommand):
    help = "Consume messages from Kafka topic"

    def handle(self, *args, **options):
        consumers = []
        no_of_consumers = 1
        kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        kafka_group_id = KAFKA_GROUP_ID
        kafka_topics = KAFKA_MIGRATION_TOPIC
        for partition in range(no_of_consumers):
            consumer = KafkaConsumer(
                kafka_bootstrap_servers, kafka_group_id, kafka_topics
            )
            consumer.process_message = custom_callback
            consumer.start()
            consumers.append(consumer)
        try:
            # Keep the main thread alive to handle interrupts
            for consumer in consumers:
                consumer.join()
        except KeyboardInterrupt:
            # Stop the Kafka consumer threads if interrupted
            for consumer in consumers:
                consumer.stop()
                consumer.join()
