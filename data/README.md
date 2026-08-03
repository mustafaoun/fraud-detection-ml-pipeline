# Data setup

The raw data and all derived parquet/database artifacts are intentionally excluded from version control. They are large, may be subject to source-data terms, and are not needed to review the project code or documented results.

## Source

Download `train_transaction.csv` and `train_identity.csv` from the [IEEE-CIS Fraud Detection competition on Kaggle](https://www.kaggle.com/c/ieee-fraud-detection/data), subject to Kaggle's terms of use.

Place both files in this directory:

```text
data/
  train_transaction.csv
  train_identity.csv
```

Then run the notebooks in the README's listed order. `src/ingestion.py` creates the local DuckDB database, and notebooks 02-04 create the derived parquet files used by subsequent stages.

Do not commit downloaded data, `fraud.db`, or the `processed/` directory.
