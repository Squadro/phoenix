from concurrent.futures import ThreadPoolExecutor

from django.core.management import BaseCommand

from constant import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, KAFKA_MIGRATION_TOPIC
from message_consumer.callbacks import custom_callback
from message_consumer.kafka_consumer import KafkaConsumer


class Command(BaseCommand):
    help = "Consume messages from Kafka topic"

    def create_consumer(self, kafka_bootstrap_servers, kafka_group_id, kafka_topics):
        consumer = KafkaConsumer(kafka_bootstrap_servers, kafka_group_id, kafka_topics)
        consumer.process_message = custom_callback
        consumer.start()
        return consumer

    def handle(self, *args, **options):
        no_of_consumers = 10
        kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        kafka_group_id = KAFKA_GROUP_ID
        kafka_topics = KAFKA_MIGRATION_TOPIC

        with ThreadPoolExecutor(max_workers=no_of_consumers) as executor:
            consumers = list(
                executor.map(
                    lambda _: self.create_consumer(
                        kafka_bootstrap_servers, kafka_group_id, kafka_topics
                    ),
                    range(no_of_consumers),
                )
            )

        try:
            # Keep the main thread alive to handle interrupts
            for consumer in consumers:
                consumer.join()
        except KeyboardInterrupt:
            # Stop the Kafka consumer threads if interrupted
            for consumer in consumers:
                consumer.stop()
                consumer.join()
