import logging
from uuid import uuid4

from confluent_kafka import Producer

import constant
from message_producer.producer_interface import MessageProducer

logger = logging.getLogger(__name__)


class KafkaProducer(MessageProducer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(KafkaProducer, cls).__new__(cls)
        return cls._instance

    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers

    def get_config(self):
        security_protocol = "PLAINTEXT"
        ssl_ca_location = getattr(constant, "KAFKA_SSL_CA_LOCATION", None)
        ssl_certificate_location = getattr(
            constant, "KAFKA_SSL_CERTIFICATE_LOCATION", None
        )
        ssl_key_location = getattr(constant, "KAFKA_SSL_KEY_LOCATION", None)
        ssl_password = getattr(constant, "KAFKA_SSL_PASSWORD", None)
        producer_config = {
            "bootstrap.servers": self.bootstrap_servers,
            "security.protocol": security_protocol,
        }
        if security_protocol == "SSL":
            producer_config.update(
                {
                    "ssl.ca.location": ssl_ca_location,
                    "ssl.certificate.location": ssl_certificate_location,
                    "ssl.key.location": ssl_key_location,
                    "ssl.key.password": ssl_password,
                }
            )
        return producer_config

    def produce_message(self, topic, message):
        producer_config = self.get_config()
        producer = Producer(producer_config)

        try:
            # Produce message to the specified topic
            producer.produce(
                topic,
                value=message,
                key=str(uuid4()),
                on_delivery=self.delivery_callback,
            )

            # Wait for any outstanding messages to be delivered and delivery reports received
            producer.flush()

            logger.info("Produced message to topic: {}".format(topic))
        except Exception as e:
            logger.exception("Error producing message: {}".format(e))
        finally:
            # Close the producer to release resources
            producer.flush()

    def delivery_callback(self, err, msg):
        if err is not None:
            logger.error("Message delivery failed: {}".format(err))
        else:
            logger.info(
                "Message delivered to {} [{}]".format(msg.topic(), msg.partition())
            )
