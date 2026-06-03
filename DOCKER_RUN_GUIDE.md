# Docker Run Guide

This project is designed to run end-to-end inside a Docker container.

## Required files before building

The repository should contain at least:

```text
app/streamlit_app.py
src/data/preprocess.py
src/models/train.py
src/models/evaluate.py
data/processed/house_sales_cleaned_for_ds570.csv
requirements.txt
Dockerfile
entrypoint.sh
.dockerignore
```

The trained model file is intentionally not stored in GitHub:

```text
models/house_price_model.joblib
```

It is generated automatically when the container starts.

## Build the image

Run this command from the repository root:

```bash
docker build -t ds570-house-price-dashboard .
```

## Run the dashboard

```bash
docker run --rm -p 8501:8501 ds570-house-price-dashboard
```

Then open:

```text
http://localhost:8501
```

## What happens inside the container?

1. The container checks whether `data/processed/house_sales_cleaned_for_ds570.csv` exists.
2. If the processed file is missing but the raw file exists, it runs `src/data/preprocess.py`.
3. It checks whether the trained model and report artifacts exist.
4. If they are missing, it runs `src/models/train.py`.
5. It starts the Streamlit dashboard.

## Expected generated files

These files are generated inside the container if missing:

```text
models/house_price_model.joblib
reports/metrics.json
reports/feature_importance.csv
reports/test_predictions.csv
```

## Why is the model not committed to GitHub?

The trained `.joblib` model is larger than GitHub's practical upload limits and is a generated artifact. Keeping it out of version control makes the project cleaner and more reproducible, because the model can be recreated from the data and training code.

## Useful local commands without Docker

Install dependencies:

```bash
pip install -r requirements.txt
```

Run training manually:

```bash
python src/models/train.py
```

Run dashboard manually:

```bash
streamlit run app/streamlit_app.py
```
