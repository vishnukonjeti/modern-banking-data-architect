import json
import time
import random
from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092', 'client.id': 'banking-load-tester'}
producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")


def run_stress_test(count=100):
    print(f"🚀 Initializing Stress Test: Sending {count} transactions...")
    start_time = time.time()

    for i in range(count):
        txn_id = f"TXN-STRESS-{i}-{random.randint(1000, 9999)}"
        data = {
            "transaction_id": txn_id,
            "user_id": f"USER_{random.randint(1, 50)}",
            "amount": round(random.uniform(10.0, 5000.0), 2),
            "timestamp": time.time()
        }

        producer.produce(
            'bank-transactions',
            key=data["user_id"],
            value=json.dumps(data),
            callback=delivery_report
        )

        # We poll to handle delivery callbacks
        producer.poll(0)

    # Wait for all messages to be delivered
    producer.flush()

    end_time = time.time()
    print(f"🏁 Finished! Sent {count} transactions in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    run_stress_test(100)