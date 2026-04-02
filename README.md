# 🏦 Modern Banking Data Architect: Resilient AI-Ledger

A production-grade prototype of a distributed financial ledger. This system is designed to handle high-volume transactions with 100% consistency, featuring self-healing infrastructure and a Generative AI forensic layer.

## 🏗️ The System Architecture
This project demonstrates a full-stack Data Engineering lifecycle:
* **Infrastructure:** [Terraform] manages Google Spanner instances as Code (IaC).
* **Database:** [Google Spanner] provides external consistency and ACID transactions.
* **Ingestion:** [Python 3.14] handles data generation with custom **Retry Logic**.
* **Resilience:** Implemented **Idempotency Keys** to prevent duplicate transactions.
* **Intelligence:** [Gemini 2.5 Flash] powers a Natural Language-to-SQL interface.

---

## 🚀 Key Features

### 1. The "Chaos" Shield (Resilience)
The system is built for real-world failures. Using `chaos_test.py`, the engine demonstrates:
* **Idempotency:** Rejects duplicate Transaction IDs to prevent double-billing.
* **Auto-Retries:** Implements a "Circuit Breaker" pattern to handle network timeouts without data loss.
* **Structured Logging:** All operations are recorded in `bank_operations.log` for auditability.

### 2. AI Financial Analyst (Intelligence)
Integrated Gemini 2.5 to bridge the gap between Big Data and Business Insights:
* **Talk-to-Bank:** Query the database using plain English (e.g., *"Show me the total of all successful transactions"*).
* **Automatic Sanitization:** Custom Python logic cleans AI-generated SQL to prevent syntax errors.

---

## 🛠️ Tech Stack
* **Language:** Python 3.14 (venv)
* **Cloud Infrastructure:** Terraform & Docker
* **Database:** Google Cloud Spanner (Emulator)
* **AI Engine:** Google Gemini 2.5 Flash API
* **Version Control:** Git & GitHub

---

## 🏃 How to Run
1. Start the infrastructure: `docker-compose up -d`
2. Apply schema: `terraform apply -auto-approve`
3. Generate data: `python data_generator.py`
4. Ask the Bank: `python talk_to_bank.py`

---
**Author:** Vishnu
**Role:** Data Architect (Portfolio Project)