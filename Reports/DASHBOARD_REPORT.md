# Step C — Streamlit Dashboard MVP Report

## Objective

Step C converts the project from a modeling pipeline into an interactive data science application. The dashboard is designed to satisfy the DS570 requirements for data visualization, interactivity, model result presentation, and end-to-end usability.

## Implemented application

Created:

```text
app/streamlit_app.py
```

The application contains six interactive tabs:

1. Overview
2. Exploratory Analysis
3. Prediction Tool
4. Model Performance
5. Affordability
6. Limitations

## Required input files

The dashboard expects the following files in the repository:

```text
data/processed/house_sales_cleaned_for_ds570.csv
models/house_price_model.joblib
reports/metrics.json
reports/feature_importance.csv
reports/test_predictions.csv
```

The app also contains fallback paths for local development from `/mnt/data`, so it can be tested in the current working environment.

## Dashboard features

### 1. Overview

Implemented summary cards for:

- Filtered listing count
- Median sale price
- Median price per square meter
- Median area

Implemented charts:

- Top districts by median sale price
- Sale price distribution

### 2. Exploratory Analysis

Implemented charts:

- Area vs sale price scatter plot
- Median price by room layout
- Monthly median sale price trend

### 3. Prediction Tool

Implemented a user input form with:

- Seller type
- City
- District
- Neighborhood
- Room layout
- Area
- Listing month
- Listing day
- Annual household income for affordability scenario

The form returns:

- Predicted sale price
- Predicted price per square meter
- District median sale price
- Price to affordability budget ratio
- Simple affordability interpretation

### 4. Model Performance

Implemented model diagnostics using Step B outputs:

- Baseline vs Random Forest metric comparison
- MAE improvement message
- Aggregated feature importance chart
- Actual vs predicted scatter plot
- Residual distribution chart

### 5. Affordability Analysis

Implemented a scenario-based affordability tool:

- User enters annual household income
- User selects affordability multiplier
- Dashboard computes an estimated affordable purchase budget
- District affordability ratios are visualized and tabulated

### 6. Limitations

Implemented a dedicated limitations page covering:

- Listing prices vs transaction prices
- Missing property-level features
- Simple affordability assumption
- Istanbul subset size limitation
- Leakage-aware exclusion of `price_per_m2`

## Data loaded by dashboard

| Item | Value |
|---|---:|
| Total rows | 15,276 |
| Total columns | 17 |
| Cities | 23 |
| Districts | 193 |
| Neighborhoods | 314 |
| Istanbul rows | 1,110 |
| Median sale price | 3,100,000 TRY |
| Median price per m² | 24,524 TRY |

## Model results displayed in dashboard

| Model | MAE | RMSE | R² | MAPE |
|---|---:|---:|---:|---:|
| City + district median baseline | 1,343,255 TRY | 2,417,259 TRY | 0.2868 | 39.52% |
| Random Forest with log target | 949,546 TRY | 1,968,067 TRY | 0.5272 | 25.37% |

The Random Forest model reduces MAE by **29.31%** compared with the baseline.

## Most important features

| Feature | Importance |
|---|---:|
| city | 0.3391 |
| area_m2 | 0.3255 |
| district | 0.1338 |
| neighborhood | 0.0720 |
| total_rooms | 0.0539 |
| listing_day | 0.0451 |
| room_layout | 0.0150 |
| rooms | 0.0077 |

## Validation performed

The Streamlit app was checked for Python syntax errors using:

```bash
python -m py_compile app/streamlit_app.py
```

Result:

```text
py_compile_ok
```

Note: Streamlit is not installed in the execution environment, so a live UI launch was not performed here. The required dependency was added to `requirements_dashboard.txt` and should be merged into the project `requirements.txt`.

## How to run locally after adding files to repo

From repository root:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Expected URL:

```text
http://localhost:8501
```

## Recommended commit

```bash
git add app/streamlit_app.py requirements.txt reports/
git commit -m "Add interactive Streamlit dashboard MVP"
```

## Next step

Step D should focus on Dockerization and reproducibility:

- Create or update `Dockerfile`
- Merge Streamlit dependencies into `requirements.txt`
- Add `docker build` and `docker run` instructions to README
- Test whether the app starts inside Docker
