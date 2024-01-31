import time

from phoenix.settings import KAFKA_BOOTSTRAP_SERVERS_IP

CLOUDFRONT_URL = "https://d23p5lga20mgs9.cloudfront.net/"
KAFKA_GROUP_ID = "reverseImageSearch"
KAFKA_CONSUMER_ENABLED = True
KAFKA_MIGRATION_TOPIC = "migration_messages"
# Kafka Producer Retry Logic
MAX_RETRIES = 3
BASE_DELAY = 1
# Default value
KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS_IP


def getCurrentTime():
    return time.strftime("%H:%M:%S", time.localtime())
