from google.cloud import spanner


def setup_emulator():
    client = spanner.Client()
    instance_id = "test-instance"
    database_id = "test-db"

    # 1. Create the Instance
    instance = client.instance(instance_id)
    if not instance.exists():
        print(f"🏗️ Creating instance {instance_id}...")
        instance.create().result()

    # 2. Create the Database (Empty)
    database = instance.database(database_id)
    if not database.exists():
        print(f"🏗️ Creating database {database_id}...")
        # In this version, we pass NOTHING to create()
        database.create().result()

        # 3. Add the Table (The DDL Step)
        print("🏗️ Creating Transactions table...")
        ddl = [
            """CREATE TABLE Transactions (
                TransactionID STRING(100) NOT NULL,
                UserID STRING(100),
                Amount FLOAT64,
                Timestamp TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp=true)
            ) PRIMARY KEY (TransactionID)"""
        ]
        database.update_ddl(ddl).result()
        print("✅ Vault Infrastructure is Ready!")
    else:
        print("✔️ Vault already exists.")

if __name__ == "__main__":
    setup_emulator()