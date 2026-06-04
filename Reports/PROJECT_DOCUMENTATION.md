# DS570 Project Documentation

## Project Title

House Sale Price Prediction & Affordability Dashboard

---

## 1. Motivation

The motivation of this project is to create a practical and reproducible data science application for housing market analysis. Housing prices are influenced by location, property size and room structure, but raw listing prices alone do not provide enough context for decision-making.

This project combines predictive modeling with an interactive dashboard so that users can both explore the market and estimate the sale price of a property.

---

## 2. Main Research Question

Can listing-level property features be used to predict house sale prices, and can these predictions be combined with a simple affordability scenario to support housing market interpretation?

---

## 3. Data

The dataset contains Turkish house sale listings with the following core variables:

- Seller type
- Area in square meters
- Room layout
- City
- District
- Neighborhood
- Listing date
- Sale price in TRY

The target variable is sale price in Turkish Lira.

---

## 4. Data Cleaning and Preprocessing

The preprocessing pipeline standardizes the data and prepares it for modeling.

Main preprocessing decisions:

- Column names are converted to consistent English names.
- Room layout is parsed into numeric room variables.
- Listing date is converted into date features.
- Unrealistic area and price values are filtered.
- Price per square meter is calculated for visualization only.
- Target-derived variables are excluded from model inputs to prevent leakage.

---

## 5. Modeling Strategy

The project compares a simple location-based baseline model with a Random Forest model.

The baseline model predicts city and district median prices.

The machine learning model uses a Random Forest Regressor with a log-transformed target. The log transformation helps because housing prices are strongly right-skewed.

---

## 6. Evaluation

The project evaluates regression performance with:

- MAE
- RMSE
- R²
- MAPE

The Random Forest model improves MAE by approximately 29.31% compared with the city and district median baseline.

---

## 7. Dashboard

The Streamlit dashboard includes:

- Market overview
- Exploratory analysis
- Prediction tool
- Model performance
- Affordability analysis
- Limitations and future work

The dashboard is designed to show both descriptive insights and predictive model results.

---

## 8. Dockerization

The project includes a Dockerfile and entrypoint script. The container checks whether the trained model exists. If the model is missing, it runs the training pipeline automatically before launching the dashboard.

This design avoids storing large model files in GitHub while keeping the project reproducible.

---

## 9. Key Contribution

The project goes beyond a standard house price prediction notebook by turning the model into a reusable dashboard application. It also adds an affordability scenario layer, allowing users to interpret predicted and median prices relative to a simple income-based budget.

---

## 10. Weaknesses

The main limitations are:

- Asking prices may differ from actual transaction prices.
- Some important housing features are unavailable.
- Affordability analysis is simplified.
- The model does not currently provide uncertainty intervals.
- Geospatial information is not included.

---

## 11. Future Improvements

Future versions could include:

- Mortgage simulation
- Interest rate assumptions
- Geocoded map views
- Neighborhood-level external indicators
- More advanced gradient boosting models
- Prediction intervals
