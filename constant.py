import os

CLOUDFRONT_URL = "https://d23p5lga20mgs9.cloudfront.net/"
KAFKA_GROUP_ID = "reverseImageSearch"
KAFKA_CONSUMER_ENABLED = True
KAFKA_MIGRATION_TOPIC = "migration_messages"
# Kafka Producer Retry Logic
MAX_RETRIES = 3
BASE_DELAY = 1
# Default value
KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

# Check if the environment is set to production
if os.environ.get("DJANGO_SETTINGS_MODULE") == "phoenix.settings_staging":
    KAFKA_BOOTSTRAP_SERVERS = "43.204.227.153"
elif os.environ.get("DJANGO_SETTINGS_MODULE") == "phoenix.settings_prod":
    KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
