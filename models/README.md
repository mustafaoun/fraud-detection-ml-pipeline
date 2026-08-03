# Model artifacts

Persisted model and preprocessing binaries are deliberately excluded from version control. Run notebooks 02 through 04 to regenerate:

- imputers and scaler
- PCA and GMM artifacts
- `xgb_model.pkl`
- `svm_model.pkl`

Notebook 05 expects the saved XGBoost model produced by Notebook 04. Model files should be versioned in an artifact store or model registry for a deployed system, not committed to a source repository.
