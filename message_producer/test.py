# DELETE -->need to delete this file
from confluent_kafka import Producer

bootstrap_servers = 'localhost:9092'

conf = {
    'bootstrap.servers': bootstrap_servers,
}


def produce_message(topic1, message1):
    producer = Producer(conf)

    try:
        # Produce message to the specified topic
        producer.produce(topic1, value=message1, callback=delivery_callback)

        # Wait for any outstanding messages to be delivered and delivery reports received
        producer.flush()

        print('Produced message to topic: {}'.format(topic))
    except Exception as e:
        print('Error producing message: {}'.format(e))
    finally:
        # Close the producer to release resources
        producer.flush()


def delivery_callback(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


topic = 'migration_messages'
message = (b'{"product_variant_id": 21106, "product_id": 14134, "image_id": 21106, "s3_key": '
           b'"Vb9LPhg3hUPia8dopvRy7SDG", "status": 21106, "product_erp_code": null}')

produce_message(topic, message)
