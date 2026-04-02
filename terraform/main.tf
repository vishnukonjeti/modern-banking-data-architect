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