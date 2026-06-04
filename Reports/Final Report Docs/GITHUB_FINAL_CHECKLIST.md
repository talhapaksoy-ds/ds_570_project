# GitHub Final Checklist

Use this list directly before submission.

## Repository Root

The repository root should include:

```text
README.md
Dockerfile
entrypoint.sh
requirements.txt
.dockerignore
.gitignore
Makefile
DOCKER_RUN_GUIDE.md
```

## App Folder

```text
app/streamlit_app.py
```

## Source Code

```text
src/data/preprocess.py
src/models/train.py
src/models/evaluate.py
```

## Data

```text
data/processed/house_sales_cleaned_for_ds570.csv
```

## Models

```text
models/.gitkeep
```

Do not upload:

```text
models/house_price_model.joblib
```

## Reports

```text
reports/DATA_AUDIT.md
reports/MODEL_REPORT.md
reports/DASHBOARD_REPORT.md
reports/DOCKERIZATION_REPORT.md
reports/PROJECT_DOCUMENTATION.md
reports/DEMO_SCRIPT.md
reports/DS570_RUBRIC_CHECKLIST.md
```

## Final Browser Checks

Open the GitHub repository in browser and verify:

- README is visible on the main page.
- Docker instructions are visible in README.
- `Dockerfile` is in the root.
- `entrypoint.sh` is in the root.
- `app/streamlit_app.py` exists.
- `data/processed/house_sales_cleaned_for_ds570.csv` exists.
- `models/house_price_model.joblib` is not visible.
- Reports folder contains documentation files.

## Final Docker Commands

```bash
docker build -t ds570-house-price-dashboard .
docker run --rm -p 8501:8501 ds570-house-price-dashboard
```

Open:

```text
http://localhost:8501
```
