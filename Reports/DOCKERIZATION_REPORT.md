# Step D — Dockerization & Reproducibility Report

## Purpose

This step adds the containerization layer required by the DS570 final project guidelines. The goal is to make the dashboard run end-to-end inside Docker without committing the large trained model file to GitHub.

## Files created

| File | Repo location | Purpose |
|---|---|---|
| `Dockerfile` | `Dockerfile` | Builds the Python 3.11 container image, installs dependencies, copies the project, exposes Streamlit port 8501, and starts the entrypoint. |
| `entrypoint.sh` | `entrypoint.sh` | Runtime launcher. It checks for processed data, generates model/report artifacts if missing, and starts Streamlit. |
| `.dockerignore` | `.dockerignore` | Keeps large/generated/local files out of the Docker build context. |
| `requirements.txt` | `requirements.txt` | Final dependency list for dashboard, data processing, and ML training. |
| `Makefile` | `Makefile` | Optional convenience commands for local and Docker runs. |
| `DOCKER_RUN_GUIDE.md` | `DOCKER_RUN_GUIDE.md` or `docs/DOCKER_RUN_GUIDE.md` | Detailed Docker instructions. |
| `README_DOCKER_SECTION.md` | copy into `README.md` | Short README section for Docker usage. |

## Runtime behavior

The container follows this sequence:

1. Create `models/`, `reports/`, and `data/processed/` if they do not exist.
2. Check whether `data/processed/house_sales_cleaned_for_ds570.csv` exists.
3. If processed data is missing but raw data exists, run `src/data/preprocess.py`.
4. Check whether model/report artifacts exist.
5. If missing, run `src/models/train.py`.
6. Start the dashboard with Streamlit on `0.0.0.0:8501`.

## Generated files not committed to GitHub

These files are intentionally generated at runtime and should not be committed:

```text
models/house_price_model.joblib
reports/metrics.json
reports/feature_importance.csv
reports/test_predictions.csv
```

This resolves the GitHub upload problem caused by the large `.joblib` file and improves reproducibility.

## Docker commands

Build:

```bash
docker build -t ds570-house-price-dashboard .
```

Run:

```bash
docker run --rm -p 8501:8501 ds570-house-price-dashboard
```

Open:

```text
http://localhost:8501
```

## Validation performed in this environment

Docker is not installed in the current execution environment, so a full image build could not be executed here. The following checks were completed:

```text
entrypoint.sh shell syntax: OK
required Docker files: present
```

The Docker build should be tested on a local machine with Docker Desktop installed.

## Recommended commit message

```bash
git add .
git commit -m "Add Docker containerization for reproducible dashboard run"
```
