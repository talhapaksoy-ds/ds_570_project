Project Title

Objective
  What problem is solved
  Why it matters
  Expected outcome

Features
  Automated data ingestion
  Data preprocessing pipeline
  Exploratory visualizations
  Machine learning prediction
  Interactive dashboard
  Dockerized deployment

Installation
  git clone ...
  cd project

Docker Setup
  docker build -t ds-project .
  docker run -p 8050:8050 ds-project
  
Technologies
  Python
  Pandas
  Scikit-learn
  Plotly / Dash / Streamlit
  Docker
  
Project Status
Currently under development.

## Running the Project with Docker

The application can be built and run completely inside Docker. The trained model artifact is not committed to GitHub; it is generated automatically when the container starts.

### Build

```bash
docker build -t ds570-house-price-dashboard .
```

### Run

```bash
docker run --rm -p 8501:8501 ds570-house-price-dashboard
```

Open the dashboard at:

```text
http://localhost:8501
```

### Runtime behavior

When the container starts, `entrypoint.sh` checks whether the processed dataset and model artifacts exist. If the model is missing, it runs:

```bash
python src/models/train.py
```

Then it launches:

```bash
streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=8501
```

### Generated artifacts

The following files are generated automatically and should not be committed:

```text
models/house_price_model.joblib
reports/metrics.json
reports/feature_importance.csv
reports/test_predictions.csv
```
