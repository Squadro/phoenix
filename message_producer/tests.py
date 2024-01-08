import unittest
from unittest.mock import patch
from message_producer.kafka_producer import KafkaProducer  # Import your actual KafkaProducer class
from constant import KAFKA_BOOTSTRAP_SERVERS


class KafkaProducerTestCase(unittest.TestCase):
    @patch('message_producer.kafka_producer.KafkaProducer')
    def test_produce_kafka_message(self, mock_kafka_producer):
        # Mock the KafkaProducer class to avoid connecting to a real Kafka broker during testing
        kafka_producer_instance = mock_kafka_producer.return_value

        # Set up your test data or conditions
        test_topic = 'your_test_topic'
        test_message = 'your_test_message'

        # Create an instance of your KafkaProducer class
        kafka_producer = KafkaProducer(KAFKA_BOOTSTRAP_SERVERS)

        # Call the produce_message method with the test data
        kafka_producer.produce_message(test_topic, test_message)

        # Assert that the produce method of the Kafka producer is called with the correct arguments
        kafka_producer_instance.produce.assert_called_once_with(test_topic, key=None, value=test_message)

    # Add more test methods as needed


if __name__ == '__main__':
    unittest.main()
