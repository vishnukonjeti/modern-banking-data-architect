import logging
import os
import time
from google.cloud import spanner
from google.api_core import exceptions

# 1. Setup the Black Box Logger
logging.basicConfig(
    filename='../logs/bank_operations.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

os.environ["SPANNER_EMULATOR_HOST"] = "localhost:9010"


def process_payment(transaction_id, amount):
    """The Worker: Attempts a single database insertion."""
    client = spanner.Client(project="local-banking-project")
    instance = client.instance("bank-master")
    database = instance.database("transaction-ledger")

    def insert_payment(transaction):
        transaction.insert(
            table="Transactions",
            columns=("Id", "Amount", "Status"),
            values=[(transaction_id, amount, "SUCCESS")],
        )

    database.run_in_transaction(insert_payment)


def process_with_retry(transaction_id, amount, retries=3):
    """The Architect: Handles network chaos and retries."""
    for attempt in range(retries):
        try:
            process_payment(transaction_id, amount)
            logging.info(f"SUCCESS: ID {transaction_id} finalized on attempt {attempt + 1}.")
            print(f"✅ Transaction {transaction_id} processed successfully.")
            return

        except exceptions.AlreadyExists:
            logging.warning(f"IDEMPOTENCY_BLOCK: ID {transaction_id} already exists. No action taken.")
            print(f"⚠️  BLOCKING DUPLICATE: ID {transaction_id} already in ledger.")
            return

        except Exception as e:
            logging.error(f"ATTEMPT {attempt + 1} FAILED: {e}")
            print(f"🔄 Network Blip... Retrying ({attempt + 1}/{retries})")
            time.sleep(2)

    print("❌ FATAL: All retries failed.")


if __name__ == "__main__":
    # Test Case 1: Standard Success
    new_id = 77777777
    process_with_retry(new_id, 1500.0)

    # Test Case 2: The 'Double Click' (Idempotency Test)
    print("\n--- Simulating User Double-Click ---")
    process_with_retry(new_id, 1500.0)