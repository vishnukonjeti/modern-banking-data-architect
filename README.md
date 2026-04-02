# 🏦 Modern Banking Data Architect: Resilient AI-Ledger

A production-grade prototype of a distributed financial ledger. This system is designed to handle high-volume transactions with 100% consistency, featuring self-healing infrastructure and a Generative AI forensic auditing layer.

---

## 🏗️ The System Architecture
This project demonstrates a full-stack Data Engineering lifecycle:
* **Database:** [Google Spanner] Distributed SQL with External Consistency.
* **Infrastructure:** [Terraform] Infrastructure-as-Code (IaC) for reproducible environments.
* **Ingestion:** [Python 3.14] Handles data generation with custom **Retry Logic**.
* **Resilience:** Implemented **Idempotency Keys** to prevent duplicate transactions.
* **Intelligence:** [Gemini 2.5 Flash] Powers a Natural Language-to-SQL interface.



---

## 🚀 Key Features

### 1. The "Chaos" Shield (Resilience)
The system is built for real-world failures. Using `scripts/chaos_test.py`, the engine demonstrates:
* **Idempotency:** Automatically detects and rejects duplicate Transaction IDs to prevent double-billing.
* **Auto-Retries:** Implements a "Circuit Breaker" pattern (Exponential Backoff) to handle network timeouts without data loss.
* **Structured Logging:** All operations are recorded in `logs/bank_operations.log` for legal auditing.

### 2. AI Financial Analyst (Intelligence)
Integrated Gemini 2.5 to bridge the gap between Big Data and Business Insights:
* **Talk-to-Bank:** Query the database using plain English (e.g., *"Show me the total of all successful transactions"*).
* **Sanitization Layer:** Custom Python logic cleans AI-generated SQL to ensure safe execution on the ledger.

---

## 📁 Project Structure
```text
modern-banking-data-architect/
├── terraform/          # Infrastructure-as-Code (Database Schema)
├── scripts/            # Python Engines (Ingestion, Chaos, AI)
├── logs/               # Audit Trails (bank_operations.log)
├── docker-compose.yml  # Local Spanner Emulator Environment
└── requirements.txt    # Python Dependencies

## 🛠️ How to Run

### 1. Infrastructure Setup
Spin up the Spanner Emulator and deploy the database schema using Terraform:

```powershell
# Start the Docker container in the background
docker-compose up -d

# Navigate to terraform directory and deploy
cd terraform
terraform init
terraform apply -auto-approve
cd ..

### 2. Data Ingestion & Testing
Populate the ledger and verify the system's resilience using the following scripts:

* **Generate Transactions:** Create 1,000 initial financial records.
    ```powershell
    python scripts/data_generator.py
    ```

* **Run Chaos Test:** Verify the database's **Idempotency** and **Retry Logic**.
    ```powershell
    python scripts/chaos_test.py
    ```

### 3. AI Intelligence Layer
Query the database using Natural Language (English to SQL) powered by Gemini:

```powershell
# Ask the Bank a question
python scripts/talk_to_bank.py