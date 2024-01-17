CLOUDFRONT_URL = "https://d23p5lga20mgs9.cloudfront.net/"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_GROUP_ID = "reverseImageSearch"
KAFKA_CONSUMER_ENABLED = True
KAFKA_MIGRATION_TOPIC = "migration_messages"
# Kafka Producer Retry Logic
MAX_RETRIES = 3
BASE_DELAY = 1
