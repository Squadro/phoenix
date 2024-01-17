# kafka_consumer.py
import json
import logging
import threading

from confluent_kafka import Consumer, KafkaException
from message_consumer.consumer_interfaces import MessageConsumer

logger = logging.getLogger(__name__)


class KafkaConsumer(threading.Thread, MessageConsumer):
    def __init__(self, bootstrap_servers, group_id, topics):
        super(KafkaConsumer, self).__init__()
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topics = topics
        self.consumer = None
        self.running = True

    def process_message(self, payload):
        # Implement the message processing logic here
        logger.info(f"Default callback received message: {payload}")

    def run(self):
        consumer_config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False  # Disable automatic commit to manage offsets manually
        }

        self.consumer = Consumer(consumer_config)
        topic = 'migration_messages'
        self.consumer.subscribe([topic])

        try:
            while self.running:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        logger.error(msg.error())
                        break
                json_data = json.loads(msg.value().decode('utf-8'))
                # Process the Kafka message using the provided callback
                self.process_message(json_data)

                # Manually commit the offset after processing the message
                self.consumer.commit(msg)


        except Exception as e:

            logger.exception(f"An error occurred: {e}")

        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def stop(self):
        self.running = False
