from confluent_kafka import Producer, KafkaError

# Kafka producer configuration
kafka_config = {"bootstrap.servers": "localhost:9092"}

# Create a Kafka producer instance
producer = Producer(kafka_config)


# Define a function to send a message to the Kafka topic
def send_to_kafka(topic, message):
    producer.produce(topic, key=None, value=message)


# Close the producer when done
producer.flush()
