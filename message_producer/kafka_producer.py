import logging
from confluent_kafka import Producer

import constant
from message_producer.interface import MessageProducer

logger = logging.getLogger(__name__)
ssl_ca_location = getattr(constant, 'KAFKA_SSL_CA_LOCATION', None)
ssl_certificate_location = getattr(constant, 'KAFKA_SSL_CERTIFICATE_LOCATION', None)
ssl_key_location = getattr(constant, 'KAFKA_SSL_KEY_LOCATION', None)
ssl_password = getattr(constant, 'KAFKA_SSL_PASSWORD', None)


def delivery_callback(err, msg):
    if err is not None:
        logger.error('Message delivery failed: {}'.format(err))
    else:
        logger.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


class KafkaProducer(MessageProducer):
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers

    def produce_message(self, topic, message):
        security_protocol = 'PLAINTEXT'
        producer_config = {
            'bootstrap.servers': self.bootstrap_servers,
            'security.protocol': security_protocol,
        }

        if security_protocol == 'SSL':
            producer_config.update({
                'ssl.ca.location': ssl_ca_location,
                'ssl.certificate.location': ssl_certificate_location,
                'ssl.key.location': ssl_key_location,
                'ssl.key.password': ssl_password,
            })

        producer = Producer(producer_config)

        try:
            # Produce message to the specified topic
            producer.produce(topic, value=message, callback=delivery_callback)

            # Wait for any outstanding messages to be delivered and delivery reports received
            producer.flush()

            logger.info('Produced message to topic: {}'.format(topic))
        except Exception as e:
            logger.exception('Error producing message: {}'.format(e))
        finally:
            # Close the producer to release resources
            producer.flush()
