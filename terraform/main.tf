variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
  default     = "local-banking-project" # This matches your Spanner Emulator setup
}

# 1. Define the Google Cloud Provider
provider "google" {
  project     = "local-banking-project"
  region      = "us-central1"

  # ADD THIS LINE: This satisfies the "Credential" check for local use
  access_token = "fake-token"

  # This tells Terraform to talk to your LOCAL laptop
  spanner_custom_endpoint = "http://localhost:9020/v1/"
}

# 2. Create the Spanner Instance
resource "google_spanner_instance" "bank_instance" {
  name         = "bank-master"
  config       = "emulator-config"
  display_name = "Main Banking Instance"
  force_destroy = true

  # The emulator requires a node count, even if it's fake
  num_nodes    = 1
}

# 3. Create the Database and the 'Ledger' Table
resource "google_spanner_database" "ledger" {
  instance = google_spanner_instance.bank_instance.name
  name     = "transaction-ledger"

  deletion_protection = false

  ddl = [
    "CREATE TABLE Transactions (Id INT64 NOT NULL, Amount FLOAT64, Status STRING(MAX)) PRIMARY KEY(Id)"
  ]
}

# # 4. Create the Writer Service Account
# resource "google_service_account" "writer_sa" {
#   account_id   = "bank-writer-sa"
#   display_name = "Service Account for Transaction Ingestion"
# }

# # 5. Create the Auditor Service Account (for AI)
# resource "google_service_account" "auditor_sa" {
#   account_id   = "bank-auditor-sa"
#   display_name = "Service Account for Read-Only AI Auditing"
# }
#
# # 6. Grant WRITER permissions to the Writer SA
# resource "google_spanner_database_iam_member" "writer_role" {
#   project  = var.project_id
#   instance = google_spanner_instance.bank_instance.name
#   database = google_spanner_database.ledger.name
#   role     = "roles/spanner.databaseUser" # Can Read/Write data
#   member   = "service_account:${google_service_account.writer_sa.email}"
# }
#
# # 7. Grant READ-ONLY permissions to the Auditor SA
# resource "google_spanner_database_iam_member" "auditor_role" {
#   project  = var.project_id
#   instance = google_spanner_instance.bank_instance.name
#   database = google_spanner_database.ledger.name
#   role     = "roles/spanner.databaseReader" # Can ONLY read
#   member   = "service_account:${google_service_account.auditor_sa.email}"
# }
