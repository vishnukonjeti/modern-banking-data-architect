import os
from google import genai
from google.cloud import spanner
from dotenv import load_dotenv
from google.api_core import exceptions

load_dotenv()
client_ai = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
os.environ["SPANNER_EMULATOR_HOST"] = "localhost:9010"


def get_answer(user_query):
    # 1. Professional Prompting (Forces uppercase to match your Day 2 data)
    prompt = f"""
    You are a SQL Expert for Google Spanner. 
    Table: 'Transactions' | Columns: 'Id' (INT64), 'Amount' (FLOAT64), 'Status' (STRING).
    Values for Status are ALWAYS uppercase: 'SUCCESS', 'FAILED', or 'PENDING'.

    User Question: {user_query}

    Return ONLY the raw SQL string. No markdown, no backticks, no explanations.
    """

    try:
        # 2. Call the AI
        sql_response = client_ai.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        raw_sql = sql_response.text.strip()

        # 3. THE SANITIZER: Strip Markdown code blocks if Gemini ignores the prompt instructions
        # This handles ```sql ... ``` or just ``` ... ```
        clean_sql = raw_sql
        if "```" in raw_sql:
            # Split by backticks and take the middle part
            parts = raw_sql.split("```")
            for part in parts:
                if "SELECT" in part.upper():
                    clean_sql = part.replace("sql", "").strip()
                    break

        print(f"🤖 AI Generated & Sanitized SQL: {clean_sql}")

        # 4. Execute on Spanner
        spanner_client = spanner.Client(project="local-banking-project")
        instance = spanner_client.instance("bank-master")
        database = instance.database("transaction-ledger")

        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(clean_sql)
            print("\n--- 🏦 BANK LEDGER RESULTS ---")
            found_data = False

            for row in results:
                found_data = True
                # DEFENSIVE CHECK: Print based on how many columns returned
                if len(row) == 1:
                    print(f"Result: {row[0]}")
                elif len(row) >= 3:
                    print(f"ID: {row[0]:<20} | Amt: ₹{row[1]:<8} | Status: {row[2]}")
                else:
                    print(f"Data: {row}")

            if not found_data:
                print("No records found matching that query.")

    except exceptions.ResourceExhausted:
        print("🚦 API Quota Full. Please wait 60 seconds for the Free Tier to reset.")

    except Exception as e:
        # Catch syntax errors (like if the AI hallucinates a column name)
        print(f"❌ System Error: {e}")


if __name__ == "__main__":
    while True:
        query = input("\n💬 Ask the Bank a question (or 'exit'): ")
        if query.lower() == 'exit': break
        try:
            get_answer(query)
        except Exception as e:
            print(f"❌ Error: {e}")