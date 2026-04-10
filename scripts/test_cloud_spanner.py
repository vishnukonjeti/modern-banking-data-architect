from google.cloud import spanner

# 1. Setup - Replace with your project ID
project_id = "modern-banking-architect"
instance_id = "banking-instance"
database_id = "banking-db"

client = spanner.Client(project=project_id)
instance = client.instance(instance_id)
database = instance.database(database_id)

def check_connection():
    try:
        # Just try a simple select
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql("SELECT 1")
            for row in results:
                print("✅ Successfully connected to Real Cloud Spanner!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_connection()