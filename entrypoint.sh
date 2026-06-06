#!/bin/sh

set -eu

echo "Starting DS570 House Price Dashboard container..."

mkdir -p models
mkdir -p reports

if [ ! -f "data/processed/house_sales_cleaned_for_ds570.csv" ]; then
    echo "Processed data file was not found."
    echo "Checking whether raw data exists..."

    if [ -f "data/raw/processed_turkish_house_sales.csv" ]; then
        echo "Raw data found. Running preprocessing pipeline..."
        python src/data/preprocess.py
    else
        echo "No processed or raw data file found."
        echo "Expected one of the following files:"
        echo "data/processed/house_sales_cleaned_for_ds570.csv"
        echo "data/raw/processed_turkish_house_sales.csv"
        exit 1
    fi
else
    echo "Processed data found."
fi

if [ ! -f "models/house_price_model.joblib" ]; then
    echo "Model file not found. Training model..."
    python src/models/train.py
else
    echo "Model file found."
fi

echo "Starting Streamlit dashboard..."

streamlit run app/streamlit_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501
