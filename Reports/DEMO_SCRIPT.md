# 10-Minute Oral Demo Script

## 0:00 – 1:00 | Introduction

This project is an end-to-end data science application for house sale price prediction and affordability analysis. The goal is to estimate property sale prices using listing-level features and present the results through an interactive dashboard.

The project is not a static notebook. It includes data processing, visualization, machine learning, model evaluation, dashboard interactivity, Git organization and Docker containerization.

---

## 1:00 – 2:00 | Problem and Motivation

Housing prices are difficult to interpret because they depend heavily on location, area and property structure. A raw listing price does not immediately tell us whether a property is high or low compared with similar listings.

This project answers two main questions:

1. Can we predict sale prices from property features?
2. Can we use those predictions to support a simple affordability analysis?

---

## 2:00 – 3:00 | Data

The dataset contains Turkish house sale listings. The main columns are seller type, area, room layout, city, district, neighborhood, listing date and price.

The target variable is sale price in TRY.

An important limitation is that these are asking prices, not completed transaction prices.

---

## 3:00 – 4:00 | Data Processing

The preprocessing pipeline standardizes column names, parses room layouts such as 3+1, creates date features and applies domain-based filters.

The project also calculates price per square meter for analysis, but this variable is not used in the model because it is derived from the target and would cause data leakage.

---

## 4:00 – 5:00 | Modeling

I compare two approaches.

The baseline model is a city and district median price predictor. This is meaningful because location is a major driver of housing prices.

The machine learning model is a Random Forest Regressor trained on a log-transformed target. The log transformation helps because housing prices are strongly right-skewed.

---

## 5:00 – 6:00 | Model Results

The baseline model has an MAE of about 1.34 million TRY. The Random Forest model has an MAE of about 950 thousand TRY.

This means the ML model reduces MAE by about 29.31% compared with the baseline.

The most important features are city, area, district and neighborhood, which makes sense from a housing market perspective.

---

## 6:00 – 8:30 | Dashboard Demo

First, the Overview page summarizes the selected market segment.

Then, the Exploratory Analysis page shows relationships such as area vs price and median price by room layout.

The Prediction Tool allows users to enter property characteristics and get a predicted sale price.

The Model Performance page shows baseline and ML metrics, feature importance, actual vs predicted values and residuals.

The Affordability page lets users enter annual household income and compare district median prices with an estimated affordable purchase budget.

---

## 8:30 – 9:30 | Docker and Reproducibility

The project can run inside Docker.

The model file is not stored in GitHub because it is a generated artifact. Instead, the container automatically runs the training pipeline if the model is missing.

This makes the project reproducible and avoids committing large binary files.

---

## 9:30 – 10:00 | Limitations and Future Work

The main limitations are that the data contains asking prices rather than final sale prices, and some important features such as building age, heating type and floor level are not available.

Future work could include mortgage simulation, interest rate assumptions, map-based visualization and prediction intervals.
