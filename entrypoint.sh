#!/bin/sh
set -e

echo "Starting DS570 house price dashboard container..."
mkdir -p models reports data/processed

if [ ! -f "data/processed/house_sales_cleaned_for_ds570.csv" ]; then
    if [ -f "data/raw/processed_turkish_house_sales.csv" ]; then
        echo "Processed dataset not found. Running preprocessing pipeline..."
        python src/data/preprocess.py \
            --input data/raw/processed_turkish_house_sales.csv \
            --output-dir data/processed
    else
        echo "ERROR: Processed dataset not found at data/processed/house_sales_cleaned_for_ds570.csv"
        echo "ERROR: Raw fallback data/raw/processed_turkish_house_sales.csv was also not found."
        exit 1
    fi
fi

if [ ! -f "models/house_price_model.joblib" ] || [ ! -f "reports/metrics.json" ] || [ ! -f "reports/feature_importance.csv" ] || [ ! -f "reports/test_predictions.csv" ]; then
    echo "Model/report artifacts are missing. Running training pipeline..."
    python src/models/train.py
else
    echo "Existing model/report artifacts found. Skipping training."
fi

echo "Launching Streamlit dashboard on port 8501..."
exec streamlit run app/streamlit_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501
