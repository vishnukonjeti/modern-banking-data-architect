import os
from google import genai
from google.cloud import spanner
from dotenv import load_dotenv

# 1. Setup Connections
load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ["SPANNER_EMULATOR_HOST"] = "localhost:9010"


def get_ledger_data():
    """Extracts a snapshot of recent transactions for the AI."""
    spanner_client = spanner.Client(project="local-banking-project")
    instance = spanner_client.instance("bank-master")
    database = instance.database("transaction-ledger")

    with database.snapshot() as snapshot:
        # We'll pull the top 50 most recent or suspicious looking transactions
        results = snapshot.execute_sql("SELECT * FROM Transactions LIMIT 50")
        data_string = "ID | Amount | Status\n"
        for row in results:
            data_string += f"{row[0]} | ₹{row[1]} | {row[2]}\n"
    return data_string


def ask_gemini_to_audit(ledger_text):
    """Sends the raw data to Gemini for a professional audit."""
    prompt = f"""
    You are a Senior Financial Forensic Auditor. 
    Below is a snapshot of the bank's transaction ledger:

    {ledger_text}

    Please provide:
    1. A summary of the total volume processed.
    2. Identify any 'Suspicious' patterns (e.g., multiple transactions of the exact same amount).
    3. A risk rating (Low/Medium/High) for this batch.
    """

    response = client_ai.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    print("🔍 Extracting data from Spanner...")
    raw_data = get_ledger_data()

    print("🧠 Asking Gemini to analyze...")
    report = ask_gemini_to_audit(raw_data)

    print("\n" + "=" * 40)
    print("        📊 AI AUDIT REPORT             ")
    print("=" * 40)
    print(report)