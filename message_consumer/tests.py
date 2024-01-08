from django.test import TestCase

# Create your tests here.
import unittest
from unittest.mock import patch
from message_consumer.kafka_consumer import KafkaConsumer
from message_consumer.interfaces import MessageConsumer
from constant import KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID


class TestMessageConsumer(MessageConsumer):
    def consume_message(self, topic):
        return f"Consuming message from topic: {topic}"


class TestMessageConsumerTestCase(unittest.TestCase):
    def test_consume_message(self):
        # Arrange
        consumer = TestMessageConsumer()

        # Act
        result = consumer.consume_message('test_topic')

        # Assert
        expected_result = "Consuming message from topic: test_topic"
        self.assertEqual(result, expected_result)

    @patch('message_consumer.kafka_consumer.KafkaConsumer')
    def test_kafka_consume_message(self, mock_kafka_consumer):
        # Mock the KafkaConsumer class to avoid connecting to a real Kafka broker during testing
        kafka_consumer_instance = mock_kafka_consumer.return_value

        # Set up your test data or conditions
        test_topic = 'your_test_topic'
        test_message = 'your_test_message'

        # Create an instance of your KafkaConsumer class
        kafka_consumer = KafkaConsumer(KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID)

        # Call the consume_message method with the test data
        kafka_consumer.consume_message(test_topic)

        # Assert that the consume method of the Kafka consumer is called with the correct arguments
        kafka_consumer_instance.subscribe.assert_called_once_with([test_topic])
        kafka_consumer_instance.poll.assert_called_once_with(timeout_ms=1000)  # Adjust the timeout as needed
        kafka_consumer_instance.unsubscribe.assert_called_once()


if __name__ == '__main__':
    unittest.main()
