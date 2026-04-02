from google.cloud import spanner
import os

# 1. Direct Python to your local "Bank"
os.environ["SPANNER_EMULATOR_HOST"] = "localhost:9010"


def run_audit():
    # 2. Connect to the Instance and Database
    client = spanner.Client(project="local-banking-project")
    instance = client.instance("bank-master")
    database = instance.database("transaction-ledger")

    # 3. The SQL Query - Standard ANSI SQL
    # We are calculating count and volume per status (SUCCESS/FAILED/PENDING)
    query = """
    SELECT 
        Status, 
        COUNT(*) as Count, 
        SUM(Amount) as Total_Volume 
    FROM Transactions 
    GROUP BY Status
    """

    print("\n" + "=" * 40)
    print("      🏦 BANK LEDGER AUDIT REPORT      ")
    print("=" * 40)

    # 4. Use a Snapshot for a "Clean Read" (doesn't block the bank)
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(query)

        total_transactions = 0
        for row in results:
            status = row[0]
            count = row[1]
            volume = row[2]
            total_transactions += count
            print(f"Status: {status:<10} | Count: {count:<5} | Volume: ₹{volume:,.2f}")

    print("-" * 40)
    print(f"TOTAL TRANSACTIONS AUDITED: {total_transactions}")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    run_audit()