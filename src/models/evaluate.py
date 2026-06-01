"""Evaluate trained model outputs and create a short Markdown report.

Expected repo location:
    src/models/evaluate.py

Run after training:
    python src/models/evaluate.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    if len(current.parents) >= 3 and current.parents[1].name == "models":
        return current.parents[2]
    return Path.cwd()


def money(value: float) -> str:
    return f"{value:,.0f} TRY"


def pct(value: float) -> str:
    return f"{value:.2f}%"


def main() -> None:
    root = find_project_root()
    reports_dir = root / "reports"
    metrics_path = reports_dir / "metrics.json"
    predictions_path = reports_dir / "test_predictions.csv"
    importance_path = reports_dir / "feature_importance.csv"

    if not metrics_path.exists():
        raise FileNotFoundError("reports/metrics.json not found. Run src/models/train.py first.")

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    predictions = pd.read_csv(predictions_path, encoding="utf-8-sig")
    importance = pd.read_csv(importance_path, encoding="utf-8-sig")

    baseline = metrics["baseline_city_district_median"]
    model = metrics["random_forest_log_target"]
    dataset = metrics["dataset"]

    mae_improvement = (
        (baseline["MAE_TRY"] - model["MAE_TRY"]) / baseline["MAE_TRY"] * 100
    )
    rmse_improvement = (
        (baseline["RMSE_TRY"] - model["RMSE_TRY"]) / baseline["RMSE_TRY"] * 100
    )

    top_features = importance.head(8)
    top_feature_lines = "\n".join(
        f"- {row.feature}: {row.importance:.4f}"
        for row in top_features.itertuples(index=False)
    )

    worst_cases = predictions.sort_values("absolute_error_try", ascending=False).head(5)
    worst_case_lines = "\n".join(
        f"- {row.city} / {row.district} / {row.neighborhood}: "
        f"actual {money(row.actual_price_try)}, predicted {money(row.ml_prediction_try)}, "
        f"absolute error {money(row.absolute_error_try)}"
        for row in worst_cases.itertuples(index=False)
    )

    report = f"""# Model Evaluation Report

## Dataset Split

- Rows after filtering: {dataset['rows_after_filtering']:,}
- Training rows: {dataset['train_rows']:,}
- Test rows: {dataset['test_rows']:,}
- Target variable: `{dataset['target']}`
- Leakage-sensitive columns excluded from training: {', '.join(dataset['excluded_leakage_columns'])}

## Model Comparison

| Model | MAE | RMSE | R² | MAPE | SMAPE |
|---|---:|---:|---:|---:|---:|
| City + district median baseline | {money(baseline['MAE_TRY'])} | {money(baseline['RMSE_TRY'])} | {baseline['R2']:.4f} | {pct(baseline['MAPE_percent'])} | {pct(baseline['SMAPE_percent'])} |
| Random Forest, log-transformed target | {money(model['MAE_TRY'])} | {money(model['RMSE_TRY'])} | {model['R2']:.4f} | {pct(model['MAPE_percent'])} | {pct(model['SMAPE_percent'])} |

## Improvement Over Baseline

- MAE improvement: {mae_improvement:.2f}%
- RMSE improvement: {rmse_improvement:.2f}%

The baseline predicts the median sale price for each city-district pair. The machine learning model improves on that by also using area, room structure, seller type, neighborhood, and listing date features.

## Top Aggregated Feature Importances

{top_feature_lines}

## Largest Test Errors

{worst_case_lines}

## Notes and Limitations

- The current model predicts sale price, not rent, because the uploaded dataset contains house sale listings.
- `price_per_m2` is intentionally excluded from model inputs because it is derived from the target price and would create data leakage.
- The model can still make large errors for luxury listings, unusual locations, or rare property configurations.
- Future work can add richer features such as building age, floor number, transit accessibility, earthquake risk, and district-level income indicators if reliable public data is available.
"""

    output_path = reports_dir / "MODEL_REPORT.md"
    output_path.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
