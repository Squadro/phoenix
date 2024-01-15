# kafka_consumer.py
import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from message_consumer.consumer_interfaces import MessageConsumer
import constant

logger = logging.getLogger(__name__)


class KafkaConsumer(MessageConsumer):
    def __init__(self, bootstrap_servers, group_id, auto_offset_reset='earliest'):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.auto_offset_reset = auto_offset_reset

    async def consume_message(self, topic):
        if not constant.KAFKA_CONSUMER_ENABLED:
            logger.info('Kafka consumer is disabled based on the setting.')
            return
        consumer_config = {
            'bootstrap_servers': self.bootstrap_servers,
            'group_id': self.group_id,
            'auto_offset_reset': self.auto_offset_reset,
        }

        consumer = AIOKafkaConsumer(topic, loop=asyncio.get_event_loop(), **consumer_config)
        await consumer.start()

        try:
            async for msg in consumer:
                try:

                    data = json.loads(msg.value.decode('utf-8'))
                    await self.process_kafka_message(data)  # Await the task
                    logger.info(f'Task enqueued for Kafka message: {data}')
                except Exception as processing_error:
                    logger.error(f'Error processing message: {processing_error}', exc_info=True)

        except KeyboardInterrupt:
            pass
        except Exception as consumer_error:
            logger.error(f'Error in Kafka consumer: {consumer_error}', exc_info=True)
        finally:
            await consumer.stop()

    async def process_kafka_message(self, data):
        try:
            # Implement your message processing logic here
            print(f'Consumer Data:{data}')
            logger.info(f'Processing Kafka message: {data}')
            # Simulate success for demonstration purposes
            success = True

            # Mark the message as processed in the database

            return success
        except Exception as processing_error:
            logger.error(f'Error processing message: {processing_error}', exc_info=True)
            return False
