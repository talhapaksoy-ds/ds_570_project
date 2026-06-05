# DS570 Step-A Data Audit

## Decision

The uploaded file is **not a rental dataset**. It is a **Turkish house sales dataset**.

Therefore, the project should pivot from:

> Istanbul rental price prediction

to:

> **Turkish / Istanbul House Sale Price Prediction and Housing Affordability Dashboard**

This still fits the requirements because the predictive task remains a clear regression problem, the dashboard can still include affordability analysis, and the dataset is small enough to run fast inside Docker.

## Uploaded Data Summary

| Item | Value |
|---|---:|
| File | `processed_turkish_house_sales.csv` |
| Size | 1.09 MB |
| Rows | 15,276 |
| Columns | 8 |
| Missing values | 0 |
| Duplicate rows | 1,246 |
| Cities | 23 |
| Districts | 193 |
| Neighborhoods | 314 |
| Istanbul rows | 1,110 |
| Date range | 2024-04-13 to 2025-05-25 |

## Columns

Original columns:

```text
satici_tip, Metrekare, Oda_Sayisi, il, Ilce, Mahalle, Tarih, fiyat
```

Recommended normalized columns:

```text
seller_type, area_m2, room_layout, city, district, neighborhood, listing_date_raw, price_try
```

## Target Variable

The target variable should be:

```text
price_try
```

This is a **regression** target.

## Important Finding

Because only **1,110 rows** are from Istanbul, using only Istanbul as the modeling dataset may be too small. The safer project framing is:

> Train the model on all available Turkish house sales data, then provide Istanbul-focused filtering and interpretation in the dashboard.

## Price and Area Ranges

| Variable | Min | Median | Max |
|---|---:|---:|---:|
| price_try | 250,000 | 3,100,000 | 130,000,000 |
| area_m2 | 1.0 | 130.0 | 951.0 |

There are extreme values such as very small areas and very high sale prices. These should not be blindly removed, but the modeling pipeline should apply clear outlier rules.

## Recommended Initial Cleaning Rules

For the MVP model, use the following domain-based filter:

```text
20 <= area_m2 <= 500
500,000 <= price_try <= 50,000,000
room layout can be parsed
```

This keeps **15,205 rows**, or **99.54%** of the dataset.

Alternative percentile-based filter:

```text
Keep 1st–99th percentile for price and area
```

This keeps **14,773 rows**, or **96.71%**.

## Feature Engineering Applied

The following derived fields were created:

```text
rooms
living_rooms
total_rooms
listing_date
listing_month
listing_day
price_per_m2
is_model_candidate_domain
is_model_candidate_pct
```

`price_per_m2` should be used for EDA and dashboard interpretation, not as an input feature if the target is `price_try`, because it is directly derived from the target.

## Baseline Model Recommendation

Use a location-based baseline:

```text
city + district median price predictor
```

Fallback order:

```text
city + district median
city median
global median
```

This is more meaningful than a simple global average because location is central in housing price prediction.

## First ML Model Recommendation

For the first working version:

```text
RandomForestRegressor or HistGradientBoostingRegressor
```

Recommended input features for MVP:

```text
seller_type
area_m2
rooms
living_rooms
total_rooms
city
district
neighborhood
listing_month
```

## Evaluation Metrics

Use:

```text
MAE
RMSE
R²
MAPE
```

Primary metric for presentation:

```text
MAE in Turkish Lira
```

because it is easy to interpret.

## Files Produced in This Step

| File | Purpose |
|---|---|
| `house_sales_cleaned_for_ds570.csv` | Full cleaned dataset with engineered columns |
| `istanbul_house_sales_subset_for_ds570.csv` | Istanbul-only subset |
| `data_audit_summary.json` | Machine-readable audit summary |
| `DATA_AUDIT.md` | Human-readable Step-A report |

## Next Step

The next implementation step should be:

> Create `src/data/preprocess.py` in the repository and make it reproduce this cleaning pipeline from the raw CSV.
