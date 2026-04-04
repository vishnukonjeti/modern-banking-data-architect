class LedgerEngine:
    @staticmethod
    def process_transaction(db_connection, transaction_id, amount):
        """
        The 'Hardened' Logic from Phase 1.
        Validates the transaction before it ever touches the database.
        """
        # 1. Validation Logic
        if amount <= 0:
            return "❌ REJECTED: Amount must be greater than zero."

        if not transaction_id:
            return "❌ REJECTED: Transaction ID is missing."

        # 2. Database Simulation (We will link real Spanner here in Phase 3)
        # For now, we simulate a successful 'Vault' entry
        print(f"--- 🔒 Logic: Validating {transaction_id} for ${amount} ---")

        return f"✅ SUCCESS: {transaction_id} is ready for Spanner."