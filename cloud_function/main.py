import base64
import json
import functions_framework
from google.cloud import spanner

# 1. Initialize Spanner Client outside the function to reuse connections (Best Practice)
spanner_client = spanner.Client()
instance = spanner_client.instance('banking-instance')
database = instance.database('banking-db')


@functions_framework.cloud_event
def process_banking_transaction(cloud_event):
    """
    Triggered by a Pub/Sub message via Eventarc.
    Decodes the data, checks for fraud, and saves to Spanner.
    """
    try:
        # 2. Extract and Decode the Pub/Sub message
        # In Gen 2 / CloudEvents, the data is inside cloud_event.data['message']['data']
        encoded_data = cloud_event.data["message"]["data"]
        raw_json = base64.b64decode(encoded_data).decode('utf-8')
        data = json.loads(raw_json)

        # 3. Parse fields
        txn_id = data.get('transaction_id', 'N/A')
        user_id = data.get('user_id', 'UNKNOWN')
        amount = float(data.get('amount', 0))

        print(f"📥 Received Transaction: {txn_id} for User: {user_id}")

        # 🚀 PHASE 4 LOGIC: Fraud Gatekeeper
        # Reject any transaction over $500
        if amount > 500:
            print(f"🛑 REJECTED: Transaction {txn_id} exceeds $500 limit (Amount: ${amount})")
            return "Fraud Blocked", 200

        # 4. Spanner Write Operation
        def insert_transaction(transaction):
            transaction.insert(
                "Transactions",
                columns=["TransactionID", "UserID", "Amount", "Timestamp"],
                values=[(txn_id, user_id, amount, spanner.COMMIT_TIMESTAMP)]
            )

        # Execute the write within a transaction
        database.run_in_transaction(insert_transaction)

        print(f"✅ SUCCESS: {txn_id} saved to Spanner.")
        return "OK", 200

    except Exception as e:
        print(f"🔥 Error processing transaction: {str(e)}")
        # We return 200 to avoid Pub/Sub retrying a broken message indefinitely
        return "Error handled", 200