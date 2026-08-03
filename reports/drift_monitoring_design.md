# Fraud Model Drift Monitoring Design

## Purpose

Monitor the production XGBoost fraud model weekly for changes in incoming transaction behavior, model output behavior, and eventual chargeback performance. Baselines are the training and validation distributions used to release the current model.

## 1. Feature drift (weekly)

Calculate Population Stability Index (PSI) for `TransactionAmt`, `PC1` through `PC17`, and `gmm_anomaly_score`. Use the baseline bin edges and proportions from the model-release dataset so each week's result is comparable.

| PSI | Interpretation | Action |
|---|---|---|
| < 0.10 | Stable | Record and continue monitoring. |
| 0.10-0.20 | Moderate shift | Investigate the feature and check segment-level distributions. |
| > 0.20 | Material shift | Alert the model owner and begin a retraining assessment. |

Also monitor missingness, unseen categorical-code rate, and input-schema validation. A schema failure or large missingness change is an immediate data-quality incident rather than ordinary drift.

## 2. Prediction drift (daily, summarized weekly)

Track the daily distribution of predicted fraud probabilities, alert rate at the locked threshold (`0.0536`), and mean probability. Compare them with the validation baseline. A large increase in alert rate can overwhelm review operations; a large decrease can indicate under-detection or a pipeline fault.

## 3. Performance drift (when labels mature)

When chargebacks or confirmed analyst labels arrive, calculate rolling 30-day recall, precision, alert volume, and fraud dollars prevented. Report results overall and by meaningful operational segments (for example, transaction amount bands and GMM component). Labels are delayed, so performance monitoring must keep the event date and label-arrival date separate.

## 4. Retraining and rollback criteria

Start a formal retraining evaluation when any of these persist for two consecutive weekly checks:

- PSI exceeds `0.20` for `TransactionAmt`, any leading PCA component, or `gmm_anomaly_score`.
- Rolling 30-day recall falls below `85%`.
- Alert rate changes by more than 25% relative to the validation baseline without an approved business explanation.
- Input validation detects a schema or transformation mismatch.

Before deployment, evaluate a candidate on a temporally later holdout, select its threshold on validation data only, compare recall/precision/review capacity with the incumbent, and retain the incumbent model and threshold for rollback.
