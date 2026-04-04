import json
import time
from confluent_kafka import Producer

# 1. Configuration for our Armored Truck (The Producer)
conf = {
    'bootstrap.servers': 'localhost:9092',  # Pointing to our Docker Kafka
    'client.id': 'banking-app-v1'
}

# 2. Initialize the Producer
producer = Producer(conf)


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [Partition: {msg.partition()}]")


# 3. Simulate a Real-Time Transaction
def send_transaction(txn_id, user_id, amount):
    # Data is sent as a JSON 'Event'
    data = {
        "transaction_id": txn_id,
        "user_id": user_id,
        "amount": amount,
        "timestamp": time.time(),
        "status": "PENDING"
    }

    # Convert dictionary to a string (JSON)
    payload = json.dumps(data)

    # Send to the 'bank-transactions' topic
    producer.produce('bank-transactions', key=user_id, value=payload, callback=delivery_report)

    # 'Flush' forces the message out of the buffer and into the 'Highway'
    producer.flush()


if __name__ == "__main__":
    print("🚀 Starting Stream Producer...")
    # Send 3 test transactions
    send_transaction("TXN-700", "USER_VISHNU", 150.00)
    send_transaction("TXN-701", "USER_VISHNU", 25.50)
    send_transaction("TXN-702", "USER_AMAR", 3000.00)
    print("🏁 Stream complete.")