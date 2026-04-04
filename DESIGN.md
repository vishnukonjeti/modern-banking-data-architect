# 🏦 Project: Resilient Distributed Banking Ledger
**Phase 1: Foundations & Hardening** **Architect:** Vishnu  
**Status:** Production-Ready (Validated & Tested)

## 📖 Executive Summary
This project implements a globally consistent banking ledger designed for high-availability environments. The core focus of Phase 1 was moving from a "functional prototype" to a "hardened system" by implementing strict **Idempotency**, **Input Validation**, and **Automated Resilience Testing**.

---

## 🏗️ Architectural Stack
* **Database:** Google Cloud Spanner (Emulator) — Chosen for **External Consistency** and horizontal scalability.
* **Infrastructure:** Terraform — Used for "Infrastructure as Code" (IaC) to ensure environment parity.
* **Language:** Python 3.14 — Leveraging modern type-hinting and asynchronous-ready patterns.
* **Testing Suite:** Pytest with `unittest.mock` — Used for Chaos Engineering simulation.

---

## 🛡️ Key Design Decisions

### 1. External Consistency over Eventual Consistency
We chose **Google Cloud Spanner** because, in banking, "eventually correct" is not enough. By using Spanner’s **TrueTime** architecture, we ensure that every transaction is globally ordered, preventing "Double-Spend" attacks that plague standard NoSQL databases.

### 2. Idempotency (The "Unique Transaction" Rule)
To handle network retries safely, every transaction requires a UUID. 
* **The Logic:** Before any write occurs, the engine performs a "Look-aside" check.
* **The Benefit:** If a client sends the same transaction twice due to a timeout, the system rejects the second attempt as `REJECTED_DUPLICATE` rather than charging the customer twice.

### 3. Graceful Degradation & Resilience
We implemented a **Retry-with-Backoff** strategy for transient database failures.
* **Strategy:** The system attempts 3 retries on `RuntimeError`.
* **Edge Case Handling:** If the 3rd attempt fails, the system enters a `FAILED_FINAL` state, preventing infinite loops and allowing for manual auditing or "Dead Letter" queuing.

---

## 🧪 Testing & Quality Assurance
The system has been "Hardened" against 6 major failure scenarios using a Mocked Unit Test suite:

| Scenario | Risk | Mitigation | Status |
| :--- | :--- | :--- | :--- |
| **Happy Path** | System Failure | Validated end-to-end flow | ✅ PASS |
| **Duplicate ID** | Double-Charging | Idempotency Check | ✅ PASS |
| **Flaky Network** | Data Loss | 3x Retry Logic | ✅ PASS |
| **Permanent Outage** | System Hang | Max-Retry Exhaustion | ✅ PASS |
| **Malformed Input** | Security Breach | Negative Amount/Empty ID Rejection | ✅ PASS |
| **Mid-Flight Crash** | Inconsistent State | Atomic Exception Handling | ✅ PASS |

---

## 🚀 Future Roadmap: Phase 2
With a hardened consistency layer now in place, the project will move toward **Scale and Analytics**:
* **Event Streaming:** Integrating **Apache Kafka** to decouple transaction ingestion from database writes.
* **OLAP Integration:** Downstreaming ledger data to **BigQuery** for real-time AI-driven fraud detection.
* **Cloud IAM:** Transitioning from Emulator-only access to "Least Privilege" Service Accounts on Google Cloud Platform.

