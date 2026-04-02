import os
from google import genai # Changed this line
from dotenv import load_dotenv

# 1. Load your secret key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# 2. Initialize the New Client
# The client now lives under genai.Client
client = genai.Client(api_key=api_key)

try:
    # 3. Call the Brain
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain why a Data Architect is important for a bank in one sentence."
    )
    print(f"\n🤖 Gemini says: {response.text}")

except Exception as e:
    print(f"\n❌ Handshake failed: {e}")