import logging
from confluent_kafka import Consumer, KafkaError
from .interfaces import MessageConsumer

logger = logging.getLogger(__name__)


class KafkaConsumer(MessageConsumer):
    def __init__(self, bootstrap_servers, group_id, auto_offset_reset='earliest'):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset

    def consume_message(self, topic):
        consumer_config = {
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': self.auto_offset_reset,
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([topic])

        try:
            while True:
                msg = consumer.poll(1.0)  # 1.0s timeout for polling
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event, not an error
                        continue
                    else:
                        logger.error('Kafka error: {}'.format(msg.error()))
                        break

                # Process the received message
                try:
                    success = self.process_message(msg.value().decode('utf-8'))
                    if success:
                        # Acknowledge the message offset after successful processing
                        consumer.commit(message=msg)
                        logger.info('Acknowledged message offset: {}'.format(msg.offset()))
                    else:
                        logger.warning('Failed to process message: {}'.format(msg.value().decode('utf-8')))
                except Exception as e:
                    logger.exception('Error processing message: {}'.format(e))

        except KeyboardInterrupt:
            pass
        finally:
            # Close the consumer on exit
            consumer.close()

    def process_message(self, message):
        # Implement your message processing logic here
        logger.info('Processing message: {}'.format(message))
        # Simulate success for demonstration purposes
        return True
