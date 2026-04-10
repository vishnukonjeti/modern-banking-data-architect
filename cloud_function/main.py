import base64
import json
from google.cloud import spanner

# Pre-initialize the client outside the function for speed
spanner_client = spanner.Client()
instance = spanner_client.instance('banking-instance')
database = instance.database('banking-db')

def process_pubsub_message(event, context=None):
    try:
        # 1. Extract the data from the Pub/Sub envelope
        if isinstance(event, dict) and 'data' in event:
            # The message comes in as a Base64 string
            raw_data = base64.b64decode(event['data']).decode('utf-8')
            data = json.loads(raw_data)
        else:
            print("Received event with no data")
            return

        # 2. Extract values with fallbacks
        txn_id = data.get('transaction_id', 'UNKNOWN')
        user_id = data.get('user_id', 'UNKNOWN')
        amount = float(data.get('amount', 0))

        print(f"💳 Processing: {txn_id} | Amount: {amount}")

        # 3. Write to Spanner
        def insert_txn(transaction):
            transaction.insert(
                "Transactions",
                columns=["TransactionID", "UserID", "Amount", "Timestamp"],
                values=[(txn_id, user_id, amount, spanner.COMMIT_TIMESTAMP)]
            )

        database.run_in_transaction(insert_txn)
        print(f"✅ Success: {txn_id} saved to Spanner.")

    except Exception as e:
        # This will now tell us EXACTLY what went wrong in the logs
        print(f"🔥 Error details: {str(e)}")