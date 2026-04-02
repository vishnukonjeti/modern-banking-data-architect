import uuid
import random
from faker import Faker
from google.cloud import spanner
import os

# Set emulator environment
os.environ["SPANNER_EMULATOR_HOST"] = "localhost:9010"

fake = Faker()

def generate_transactions(count=1000):
    transactions = []
    for _ in range(count):
        # We use a Hash of the UUID to fit into Spanner's INT64 for now
        # (In a real bank, we'd use STRING for UUIDs, but let's stick to our schema)
        t_id = random.randint(1, 9223372036854775807)
        amount = round(random.uniform(10.0, 5000.0), 2)
        status = random.choice(['SUCCESS', 'PENDING', 'FAILED'])
        transactions.append((t_id, amount, status))
    return transactions

def insert_data(instance_id, database_id, data):
    client = spanner.Client(project="local-banking-project")
    instance = client.instance(instance_id)
    database = instance.database(database_id)

    # The "Architect" Move: Using a Batch Transaction (Mutations)
    # This is 100x faster than inserting one-by-one.
    def add_transactions(transaction):
        transaction.insert(
            table="Transactions",
            columns=("Id", "Amount", "Status"),
            values=data,
        )

    database.run_in_transaction(add_transactions)
    print(f"✅ Successfully inserted {len(data)} transactions into the Ledger.")

if __name__ == "__main__":
    records = generate_transactions(1000)
    insert_data("bank-master", "transaction-ledger", records)
