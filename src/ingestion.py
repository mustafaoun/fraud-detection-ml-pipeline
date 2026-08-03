import duckdb
import os
import sys

# Paths
DATA_DIR = "data"
TRANSACTIONS_CSV = os.path.join(DATA_DIR, "train_transaction.csv")
IDENTITY_CSV = os.path.join(DATA_DIR, "train_identity.csv")
DB_PATH = os.path.join(DATA_DIR, "fraud.db")
TMP_DIR = "tmp"

def main():
    # Check if CSV files exist
    if not os.path.exists(TRANSACTIONS_CSV):
        sys.exit(f" Error: {TRANSACTIONS_CSV} not found. Place the CSV files in the data/ directory.")
    if not os.path.exists(IDENTITY_CSV):
        sys.exit(f" Error: {IDENTITY_CSV} not found. Place the CSV files in the data/ directory.")
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # Connect to DuckDB (creates the file if it doesn't exist)
    conn = duckdb.connect(DB_PATH)
    conn.execute("SET max_memory = '4GB'")
    conn.execute(f"SET temp_directory = '{TMP_DIR}'")
    # Load transactions CSV into a table
    conn.execute("""
        CREATE OR REPLACE TABLE transactions AS
        SELECT * FROM read_csv_auto(?)
    """, (TRANSACTIONS_CSV,))

    # Load identity CSV into a table
    conn.execute("""
        CREATE OR REPLACE TABLE identity AS
        SELECT * FROM read_csv_auto(?)
    """, (IDENTITY_CSV,))

    # Create the LEFT JOIN view (keeping all transactions)
    conn.execute("""
        CREATE OR REPLACE VIEW joined_transactions AS
        SELECT t.*, i.* EXCLUDE (TransactionID)
        FROM transactions t
        LEFT JOIN identity i ON t.TransactionID = i.TransactionID
    """)

    # --- Verification ---
    transaction_count = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    identity_count = conn.execute("SELECT COUNT(*) FROM identity").fetchone()[0]
    joined_count = conn.execute("SELECT COUNT(*) FROM joined_transactions").fetchone()[0]

    print(f" Loaded transactions: {transaction_count:,} rows")
    print(f" Loaded identity: {identity_count:,} rows")
    print(f" LEFT JOIN created: {joined_count:,} rows (should match transaction count)")

    # --- Schema Documentation ---
    print("\n Schema for joined_transactions:")
    schema = conn.execute("PRAGMA table_info(joined_transactions)").fetchdf()
    print(schema[['name', 'type']].to_string(index=False))

    # --- Close connection ---
    conn.close()
    print("\n Ingestion complete. Database saved to:", DB_PATH)

if __name__ == "__main__":
    main()
