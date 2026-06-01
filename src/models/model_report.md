# Model Evaluation Report

## Dataset Split

- Rows after filtering: 13,964
- Training rows: 11,171
- Test rows: 2,793
- Target variable: `price_try`
- Leakage-sensitive columns excluded from training: is_model_candidate_domain, is_model_candidate_pct, price_per_m2

## Model Comparison

| Model | MAE | RMSE | R² | MAPE | SMAPE |
|---|---:|---:|---:|---:|---:|
| City + district median baseline | 1,343,255 TRY | 2,417,259 TRY | 0.2868 | 39.52% | 34.62% |
| Random Forest, log-transformed target | 949,546 TRY | 1,968,067 TRY | 0.5272 | 25.37% | 23.40% |

## Improvement Over Baseline

- MAE improvement: 29.31%
- RMSE improvement: 18.58%

The baseline predicts the median sale price for each city-district pair. The machine learning model improves on that by also using area, room structure, seller type, neighborhood, and listing date features.

## Top Aggregated Feature Importances

- city: 0.3391
- area_m2: 0.3255
- district: 0.1338
- neighborhood: 0.0720
- total_rooms: 0.0539
- listing_day: 0.0451
- room_layout: 0.0150
- rooms: 0.0077

## Largest Test Errors

- Istanbul / Kadıköy / Fenerbahçe: actual 48,000,000 TRY, predicted 9,223,158 TRY, absolute error 38,776,842 TRY
- Istanbul / Başakşehir / İkitelli: actual 46,800,000 TRY, predicted 9,967,478 TRY, absolute error 36,832,522 TRY
- Mugla / Datça / Köyler: actual 29,900,000 TRY, predicted 7,527,162 TRY, absolute error 22,372,838 TRY
- Mugla / Bodrum / Yalıkavak: actual 32,000,000 TRY, predicted 11,221,725 TRY, absolute error 20,778,275 TRY
- Istanbul / Kadıköy / Suadiye: actual 24,500,000 TRY, predicted 7,040,484 TRY, absolute error 17,459,516 TRY

## Notes and Limitations

- The current model predicts sale price, not rent, because the uploaded dataset contains house sale listings.
- `price_per_m2` is intentionally excluded from model inputs because it is derived from the target price and would create data leakage.
- The model can still make large errors for luxury listings, unusual locations, or rare property configurations.
- Future work can add richer features such as building age, floor number, transit accessibility, earthquake risk, and district-level income indicators if reliable public data is available.
