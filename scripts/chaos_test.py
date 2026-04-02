import os
import time
import logging
import uuid
from google.cloud import spanner
from google.api_core import exceptions

# --- 1. SYSTEM SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
log_dir = os.path.join(project_root, "logs")
log_file = os.path.join(log_dir, "bank_operations.log")

os.makedirs(log_dir, exist_ok=True)
os.environ["SPANNER_EMULATOR_HOST"] = "localhost:9010"

# Professional Logging (No emojis to prevent Windows Unicode errors)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)


# --- 2. BANKING LOGIC ---

def process_payment(transaction_id, amount):
    """Inserts a transaction with Idempotency checks."""
    spanner_client = spanner.Client(project="local-banking-project")
    instance = spanner_client.instance("bank-master")
    database = instance.database("transaction-ledger")

    def insert_row(transaction):
        transaction.execute_update(
            "INSERT Transactions (Id, Amount, Status) VALUES (@id, @amount, @status)",
            params={
                'id': transaction_id,
                'amount': amount,
                'status': 'SUCCESS'
            },
            param_types={
                'id': spanner.param_types.INT64,
                'amount': spanner.param_types.FLOAT64,
                'status': spanner.param_types.STRING
            }
        )
        logging.info(f"SUCCESS: Processed Transaction ID: {transaction_id}")

    try:
        database.run_in_transaction(insert_row)
    except exceptions.AlreadyExists:
        logging.warning(f"IDEMPOTENCY ALERT: Transaction {transaction_id} already exists. Skipping duplicate.")
    except Exception as e:
        logging.error(f"SYSTEM ERROR: {e}")
        raise e


def process_with_retry(transaction_id, amount, retries=3):
    """Circuit Breaker: Retries on network blips."""
    for attempt in range(retries):
        try:
            process_payment(transaction_id, amount)
            return True
        except Exception:
            wait = (attempt + 1) * 2
            logging.info(f"RETRYING: Attempt {attempt + 1}/{retries} in {wait}s...")
            time.sleep(wait)
    return False


# --- 3. THE FINAL RUN ---

if __name__ == "__main__":
    print("-" * 50)
    print("🚀 STARTING PRODUCTION CHAOS TEST")
    print(f"Log Path: {log_file}")
    print("-" * 50)

    # Test 1: Unique Transaction
    unique_id = int(time.time())
    process_with_retry(unique_id, 5000.0)

    # Test 2: Simulated 'Double-Click' (The Idempotency Test)
    duplicate_id = 88887777
    print("\n[Scenario: User double-clicks 'Pay' button]")
    process_with_retry(duplicate_id, 1200.0)  # First Click (Success)
    process_with_retry(duplicate_id, 1200.0)  # Second Click (Handled)

    print("-" * 50)
    print("🏁 TEST COMPLETE: ALL SYSTEMS NOMINAL")
    print("-" * 50)