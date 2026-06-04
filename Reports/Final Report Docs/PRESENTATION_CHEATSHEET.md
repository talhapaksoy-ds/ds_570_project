# Presentation Cheatsheet

## Project One-Liner

This project is a Dockerized Streamlit dashboard that predicts Turkish house sale prices and adds a simple affordability analysis layer.

---

## Main Problem

Can listing-level features such as location, area and room layout predict house sale prices, and can the prediction be used for housing affordability interpretation?

---

## Dataset

The dataset contains Turkish house sale listings.

Main variables:

```text
seller_type
area_m2
room_layout
city
district
neighborhood
listing_date
price_try
```

Target:

```text
price_try
```

---

## Models

Baseline:

```text
City + district median price predictor
```

ML model:

```text
RandomForestRegressor with log-transformed target
```

---

## Results

| Model | MAE | RMSE | R² | MAPE |
|---|---:|---:|---:|---:|
| Baseline | 1,343,255 TRY | 2,417,259 TRY | 0.2868 | 39.52% |
| Random Forest | 949,546 TRY | 1,968,067 TRY | 0.5272 | 25.37% |

Main result:

```text
Random Forest reduces MAE by approximately 29.31% compared with the baseline.
```

---

## Key Design Decisions

### Why baseline?

Location is a major price driver, so city + district median is a meaningful naive benchmark.

### Why Random Forest?

It handles nonlinear relationships and mixed feature effects well, while staying easy to explain.

### Why log target?

Housing prices are right-skewed. Log transformation reduces the impact of very expensive listings.

### Why exclude price_per_m2?

`price_per_m2 = price_try / area_m2`, so including it would leak target information.

### Why Docker?

Docker ensures that classmates and the instructor can run the app in the same environment.

### Why not store the model file?

The `.joblib` file is generated automatically by `train.py`. This keeps the repository smaller and more reproducible.

---

## Strongest Dashboard Demo Flow

1. Overview tab: show market summary.
2. Exploratory Analysis tab: show area vs price.
3. Prediction Tool tab: enter an example Istanbul property and predict.
4. Model Performance tab: show baseline vs ML metrics.
5. Affordability tab: enter income and explain the ratio.
6. Limitations tab: show awareness of weaknesses.

---

## Limitations to Mention

- Asking prices are not final transaction prices.
- Important features such as building age, heating type and floor level are missing.
- Affordability analysis is simplified.
- The model does not yet provide prediction intervals.
- No map visualization yet.

---

## Future Work

- Add mortgage and interest rate simulation.
- Add geocoded map visualization.
- Add neighborhood socioeconomic indicators.
- Compare with gradient boosting.
- Add uncertainty estimates.
