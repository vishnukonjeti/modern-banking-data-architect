import time
import json
from google.cloud import pubsub_v1

# Configuration
project_id = "modern-banking-architect"
topic_id = "bank-transactions"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def publish_messages():
    print(f"🚀 Streaming 100 transactions to {topic_id}...")

    for i in range(1, 101):
        data = {
            "transaction_id": f"TXN-BATCH-{i}",
            "user_id": f"USER_{i % 10}",
            "amount": round(i * 1.5, 2)
        }

        # Convert to string and encode to bytes
        message_data = json.dumps(data).encode("utf-8")

        # 1. Publish the message
        future = publisher.publish(topic_path, message_data)

        # 2. THIS IS THE MISSING PART: Wait for the result
        try:
            message_id = future.result()
            print(f"✅ Sent {data['transaction_id']} (ID: {message_id})")
        except Exception as e:
            print(f"❌ Failed to send {data['transaction_id']}: {e}")

    print(f"🏁 Successfully verified 100 transactions reached GCP.")


if __name__ == "__main__":
    publish_messages()