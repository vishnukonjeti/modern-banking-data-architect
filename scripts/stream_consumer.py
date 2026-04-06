import json
from confluent_kafka import Consumer
from google.cloud import spanner
from google.api_core import exceptions  # <--- Make sure this import is here!
from ledger_engine import LedgerEngine

# 1. Setup Spanner Connection (Emulator)
spanner_client = spanner.Client()
instance = spanner_client.instance("test-instance")
database = instance.database("test-db")

# 2. Kafka Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'ledger-processors',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['bank-transactions'])


def save_to_spanner(transaction_id, user_id, amount):
    """ The final step: Locking the data in the vault with a duplicate check. """
    try:
        def insert_txn(transaction):
            transaction.execute_update(
                "INSERT INTO Transactions (TransactionID, UserID, Amount, Timestamp) "
                "VALUES (@tid, @uid, @amt, PENDING_COMMIT_TIMESTAMP())",
                params={'tid': transaction_id, 'uid': user_id, 'amt': amount},
                param_types={
                    'tid': spanner.param_types.STRING,
                    'uid': spanner.param_types.STRING,
                    'amt': spanner.param_types.FLOAT64
                }
            )

        database.run_in_transaction(insert_txn)
        print(f"🏛️ Vault Locked: {transaction_id} saved to Spanner.")

    except exceptions.AlreadyExists:
        # This is the "Idempotency" magic - it prevents double-charging!
        print(f"⏭️ Skipping {transaction_id}: Already exists in the Vault.")


def process_stream():
    print("🎧 Consumer is listening for transactions...")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None: continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # --- THE SAFETY NET ---
            raw_payload = msg.value()
            if not raw_payload:
                print("⚠️ Skipping empty message.")
                continue

            try:
                data = json.loads(raw_payload.decode('utf-8'))
            except json.JSONDecodeError:
                print(f"❌ Failed to decode JSON: {raw_payload}")
                continue
            # -----------------------

            # Use Phase 1 Brain to Validate
            validation_status = LedgerEngine.process_transaction(
                db_connection=None,
                transaction_id=data['transaction_id'],
                amount=data['amount']
            )

            if "SUCCESS" in validation_status:
                save_to_spanner(data['transaction_id'], data['user_id'], data['amount'])
            else:
                print(f"⚠️ Validation Failed: {validation_status}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    process_stream()