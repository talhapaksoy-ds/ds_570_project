"""Streamlit dashboard for the DS570 Turkish house sale price project.

Expected repo location:
    app/streamlit_app.py

Run from the repository root:
    streamlit run app/streamlit_app.py

The app expects the processed data file:
    data/processed/house_sales_cleaned_for_ds570.csv

The model and report artifacts are generated automatically if missing:
    models/house_price_model.joblib
    reports/metrics.json
    reports/feature_importance.csv
    reports/test_predictions.csv

It also contains fallback paths for local development in /mnt/data.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

APP_TITLE = "House Sale Price Prediction & Affordability Dashboard"
TARGET_COLUMN = "price_try"
MODEL_FEATURES = [
    "seller_type",
    "room_layout",
    "city",
    "district",
    "neighborhood",
    "area_m2",
    "rooms",
    "living_rooms",
    "total_rooms",
    "listing_month",
    "listing_day",
]


def project_root() -> Path:
    """Resolve project root from app location or current working directory."""
    current = Path(__file__).resolve()
    # repo/app/streamlit_app.py -> repo
    if len(current.parents) >= 2 and current.parent.name == "app":
        return current.parents[1]
    return Path.cwd()


ROOT = project_root()


def find_file(candidates: Iterable[Path]) -> Optional[Path]:
    """Return the first existing file from a list of candidate paths."""
    for path in candidates:
        if path.exists():
            return path
    return None


DATA_CANDIDATES = [
    ROOT / "data" / "processed" / "house_sales_cleaned_for_ds570.csv",
    ROOT / "house_sales_cleaned_for_ds570.csv",
    Path("/mnt/data/house_sales_cleaned_for_ds570.csv"),
]
MODEL_CANDIDATES = [
    ROOT / "models" / "house_price_model.joblib",
    ROOT / "model_artifacts" / "house_price_model.joblib",
    Path("/mnt/data/model_artifacts/house_price_model.joblib"),
]
METRICS_CANDIDATES = [
    ROOT / "reports" / "metrics.json",
    ROOT / "metrics.json",
    Path("/mnt/data/metrics.json"),
]
FEATURE_IMPORTANCE_CANDIDATES = [
    ROOT / "reports" / "feature_importance.csv",
    ROOT / "feature_importance.csv",
    Path("/mnt/data/feature_importance.csv"),
]
PREDICTIONS_CANDIDATES = [
    ROOT / "reports" / "test_predictions.csv",
    ROOT / "test_predictions.csv",
    Path("/mnt/data/test_predictions.csv"),
]
TRAIN_SCRIPT_CANDIDATES = [
    ROOT / "src" / "models" / "train.py",
    ROOT / "train.py",
    Path("/mnt/data/train.py"),
]

DATA_PATH = find_file(DATA_CANDIDATES)
MODEL_PATH = find_file(MODEL_CANDIDATES)
METRICS_PATH = find_file(METRICS_CANDIDATES)
FEATURE_IMPORTANCE_PATH = find_file(FEATURE_IMPORTANCE_CANDIDATES)
PREDICTIONS_PATH = find_file(PREDICTIONS_CANDIDATES)
TRAIN_SCRIPT_PATH = find_file(TRAIN_SCRIPT_CANDIDATES)


def refresh_artifact_paths() -> None:
    """Refresh global paths after training creates new artifacts."""
    global MODEL_PATH, METRICS_PATH, FEATURE_IMPORTANCE_PATH, PREDICTIONS_PATH
    MODEL_PATH = find_file(MODEL_CANDIDATES)
    METRICS_PATH = find_file(METRICS_CANDIDATES)
    FEATURE_IMPORTANCE_PATH = find_file(FEATURE_IMPORTANCE_CANDIDATES)
    PREDICTIONS_PATH = find_file(PREDICTIONS_CANDIDATES)


def ensure_training_artifacts() -> bool:
    """Train the model automatically if generated artifacts are missing.

    The model file is intentionally not stored in Git because it can be large.
    This function keeps the app reproducible by generating the model and
    reports from the committed training script and processed data.
    """
    required_paths = [MODEL_PATH, METRICS_PATH, FEATURE_IMPORTANCE_PATH, PREDICTIONS_PATH]
    if all(path is not None for path in required_paths):
        return True

    if TRAIN_SCRIPT_PATH is None:
        st.error(
            "Training artifacts are missing and src/models/train.py was not found. "
            "Add the training script to the repository, then rerun the app."
        )
        return False

    with st.spinner("Model artifacts were not found. Training the model now..."):
        try:
            subprocess.run(
                [sys.executable, str(TRAIN_SCRIPT_PATH)],
                cwd=str(ROOT),
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            st.error("Automatic model training failed.")
            if exc.stdout:
                st.code(exc.stdout, language="text")
            if exc.stderr:
                st.code(exc.stderr, language="text")
            return False

    refresh_artifact_paths()
    missing_after_training = [
        name
        for name, path in {
            "model": MODEL_PATH,
            "metrics": METRICS_PATH,
            "feature importance": FEATURE_IMPORTANCE_PATH,
            "test predictions": PREDICTIONS_PATH,
        }.items()
        if path is None
    ]

    if missing_after_training:
        st.error(
            "Training finished, but these expected artifacts are still missing: "
            + ", ".join(missing_after_training)
        )
        return False

    return True


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    """Load and lightly type-cast processed housing data."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    if "listing_date" in df.columns:
        df["listing_date"] = pd.to_datetime(df["listing_date"], errors="coerce")
    return df


@st.cache_resource(show_spinner=False)
def load_model(path: str) -> Any:
    """Load the fitted sklearn model."""
    return joblib.load(path)


@st.cache_data(show_spinner=False)
def load_json(path: str) -> Dict[str, Any]:
    """Load JSON report file."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data(show_spinner=False)
def load_csv(path: str) -> pd.DataFrame:
    """Load CSV report file."""
    return pd.read_csv(path, encoding="utf-8-sig")


def format_try(value: float) -> str:
    """Format Turkish lira values for display."""
    if pd.isna(value):
        return "N/A"
    return f"{value:,.0f} TRY".replace(",", ".")


def parse_room_layout(room_layout: str) -> tuple[float, float, float]:
    """Parse room layout values such as 3+1 or 3.5+1."""
    try:
        left, right = str(room_layout).replace(",", ".").split("+")[:2]
        rooms = float(left)
        living_rooms = float(right)
        return rooms, living_rooms, rooms + living_rooms
    except Exception:
        return np.nan, np.nan, np.nan


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters and return the selected subset."""
    st.sidebar.header("Filters")

    cities = sorted(df["city"].dropna().unique().tolist())
    default_city_index = cities.index("Istanbul") if "Istanbul" in cities else 0
    selected_city = st.sidebar.selectbox("City", cities, index=default_city_index)

    city_df = df[df["city"] == selected_city].copy()
    districts = ["All"] + sorted(city_df["district"].dropna().unique().tolist())
    selected_district = st.sidebar.selectbox("District", districts)

    filtered = city_df.copy()
    if selected_district != "All":
        filtered = filtered[filtered["district"] == selected_district]

    room_options = ["All"] + sorted(filtered["room_layout"].dropna().unique().tolist())
    selected_room = st.sidebar.selectbox("Room layout", room_options)
    if selected_room != "All":
        filtered = filtered[filtered["room_layout"] == selected_room]

    min_area = int(max(1, np.floor(df["area_m2"].min())))
    max_area = int(np.ceil(df["area_m2"].max()))
    selected_area = st.sidebar.slider(
        "Area range, m²",
        min_value=min_area,
        max_value=max_area,
        value=(min_area, min(250, max_area)),
        step=5,
    )
    filtered = filtered[
        (filtered["area_m2"] >= selected_area[0]) &
        (filtered["area_m2"] <= selected_area[1])
    ]

    return filtered


def overview_tab(df: pd.DataFrame, filtered: pd.DataFrame) -> None:
    """Render overview and market summary."""
    st.subheader("Market overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filtered listings", f"{len(filtered):,}".replace(",", "."))
    c2.metric("Median price", format_try(filtered[TARGET_COLUMN].median()))
    c3.metric("Median price per m²", format_try(filtered["price_per_m2"].median()))
    c4.metric("Median area", f"{filtered['area_m2'].median():.0f} m²" if len(filtered) else "N/A")

    if filtered.empty:
        st.warning("No listings match the selected filters.")
        return

    st.markdown(
        "This page summarizes the selected market segment. The dashboard is based on "
        "cleaned sale listings and is designed to support exploratory analysis, model "
        "inspection and affordability scenarios."
    )

    district_summary = (
        filtered.groupby("district", as_index=False)
        .agg(
            median_price_try=(TARGET_COLUMN, "median"),
            median_price_per_m2=("price_per_m2", "median"),
            listing_count=(TARGET_COLUMN, "size"),
        )
        .sort_values("median_price_try", ascending=False)
        .head(20)
    )

    fig = px.bar(
        district_summary,
        x="district",
        y="median_price_try",
        hover_data=["listing_count", "median_price_per_m2"],
        title="Top districts by median sale price",
        labels={
            "district": "District",
            "median_price_try": "Median sale price, TRY",
            "listing_count": "Listings",
            "median_price_per_m2": "Median price per m², TRY",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    fig_hist = px.histogram(
        filtered,
        x=TARGET_COLUMN,
        nbins=60,
        title="Sale price distribution",
        labels={TARGET_COLUMN: "Sale price, TRY"},
    )
    st.plotly_chart(fig_hist, use_container_width=True)


def eda_tab(filtered: pd.DataFrame) -> None:
    """Render exploratory data analysis charts."""
    st.subheader("Exploratory analysis")
    if filtered.empty:
        st.warning("No listings match the selected filters.")
        return

    fig_scatter = px.scatter(
        filtered,
        x="area_m2",
        y=TARGET_COLUMN,
        color="room_layout",
        hover_data=["city", "district", "neighborhood", "seller_type"],
        title="Area and sale price relationship",
        labels={"area_m2": "Area, m²", TARGET_COLUMN: "Sale price, TRY", "room_layout": "Room layout"},
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    room_summary = (
        filtered.groupby("room_layout", as_index=False)
        .agg(median_price_try=(TARGET_COLUMN, "median"), listing_count=(TARGET_COLUMN, "size"))
        .sort_values("median_price_try", ascending=False)
    )
    fig_room = px.bar(
        room_summary,
        x="room_layout",
        y="median_price_try",
        hover_data=["listing_count"],
        title="Median price by room layout",
        labels={"room_layout": "Room layout", "median_price_try": "Median sale price, TRY"},
    )
    st.plotly_chart(fig_room, use_container_width=True)

    monthly_summary = (
        filtered.dropna(subset=["listing_date"])
        .assign(month=lambda x: x["listing_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(median_price_try=(TARGET_COLUMN, "median"), listing_count=(TARGET_COLUMN, "size"))
    )
    if not monthly_summary.empty:
        fig_month = px.line(
            monthly_summary,
            x="month",
            y="median_price_try",
            markers=True,
            hover_data=["listing_count"],
            title="Monthly median sale price trend",
            labels={"month": "Listing month", "median_price_try": "Median sale price, TRY"},
        )
        st.plotly_chart(fig_month, use_container_width=True)


def prediction_tab(df: pd.DataFrame, model: Any | None) -> None:
    """Render prediction form and affordability scenario."""
    st.subheader("Prediction tool")
    st.markdown(
        "Enter property characteristics to estimate a sale price. The model uses a leakage-safe "
        "pipeline trained on location, area, room layout, seller type and listing date features."
    )

    if model is None:
        st.error(
            "Model could not be loaded. The app tried to generate the model automatically, "
            "but the model artifact is still unavailable."
        )
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        seller_type = st.selectbox("Seller type", sorted(df["seller_type"].dropna().unique().tolist()))
        city_options = sorted(df["city"].dropna().unique().tolist())
        city_index = city_options.index("Istanbul") if "Istanbul" in city_options else 0
        city = st.selectbox("City", city_options, index=city_index)
        districts = sorted(df.loc[df["city"] == city, "district"].dropna().unique().tolist())
        district = st.selectbox("District", districts)
    with col2:
        neighborhoods = sorted(
            df.loc[(df["city"] == city) & (df["district"] == district), "neighborhood"]
            .dropna()
            .unique()
            .tolist()
        )
        neighborhood = st.selectbox("Neighborhood", neighborhoods if neighborhoods else ["Unknown"])
        room_layout = st.selectbox("Room layout", sorted(df["room_layout"].dropna().unique().tolist()))
        area_m2 = st.number_input("Area, m²", min_value=20.0, max_value=500.0, value=100.0, step=5.0)
    with col3:
        listing_month = st.slider("Listing month", min_value=1, max_value=12, value=5)
        listing_day = st.slider("Listing day", min_value=1, max_value=31, value=15)
        annual_income = st.number_input(
            "Annual household income for affordability scenario, TRY",
            min_value=0,
            value=1_200_000,
            step=50_000,
        )

    rooms, living_rooms, total_rooms = parse_room_layout(room_layout)
    model_input = pd.DataFrame(
        [
            {
                "seller_type": seller_type,
                "room_layout": room_layout,
                "city": city,
                "district": district,
                "neighborhood": neighborhood,
                "area_m2": float(area_m2),
                "rooms": rooms,
                "living_rooms": living_rooms,
                "total_rooms": total_rooms,
                "listing_month": int(listing_month),
                "listing_day": int(listing_day),
            }
        ],
        columns=MODEL_FEATURES,
    )

    if st.button("Predict sale price", type="primary"):
        prediction = float(np.maximum(model.predict(model_input)[0], 0))
        selected_market = df[(df["city"] == city) & (df["district"] == district)]
        district_median = float(selected_market[TARGET_COLUMN].median()) if len(selected_market) else np.nan
        price_per_m2 = prediction / area_m2
        affordable_budget = annual_income * 4.0
        affordability_ratio = prediction / affordable_budget if affordable_budget > 0 else np.nan

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Predicted price", format_try(prediction))
        r2.metric("Predicted price per m²", format_try(price_per_m2))
        r3.metric("District median", format_try(district_median))
        r4.metric("Price / affordability budget", f"{affordability_ratio:.2f}x" if pd.notna(affordability_ratio) else "N/A")

        if pd.notna(affordability_ratio):
            if affordability_ratio <= 1:
                st.success("The predicted price is within the selected affordability budget.")
            elif affordability_ratio <= 1.5:
                st.warning("The predicted price is moderately above the selected affordability budget.")
            else:
                st.error("The predicted price is substantially above the selected affordability budget.")

        st.caption(
            "Affordability budget is approximated as four times annual household income. "
            "This is a simple scenario metric for comparison, not financial advice."
        )

        with st.expander("Model input row"):
            st.dataframe(model_input, use_container_width=True)


def model_performance_tab(metrics: Dict[str, Any] | None, feature_importance: pd.DataFrame | None, predictions: pd.DataFrame | None) -> None:
    """Render model metrics, feature importance and prediction diagnostics."""
    st.subheader("Model performance")

    if metrics is None:
        st.error("metrics.json was not found. Run src/models/train.py first.")
        return

    baseline = metrics["baseline_city_district_median"]
    model = metrics["random_forest_log_target"]

    metric_rows = pd.DataFrame(
        [
            {"Model": "City + district median baseline", **baseline},
            {"Model": "Random Forest with log target", **model},
        ]
    )
    st.dataframe(metric_rows, use_container_width=True)

    improvement = 100 * (baseline["MAE_TRY"] - model["MAE_TRY"]) / baseline["MAE_TRY"]
    st.info(f"The Random Forest model reduces MAE by {improvement:.2f}% compared with the baseline.")

    if feature_importance is not None and not feature_importance.empty:
        top_features = feature_importance.sort_values("importance", ascending=False).head(12)
        fig = px.bar(
            top_features,
            x="feature",
            y="importance",
            title="Aggregated feature importance",
            labels={"feature": "Feature", "importance": "Importance"},
        )
        st.plotly_chart(fig, use_container_width=True)

    if predictions is not None and not predictions.empty:
        sample = predictions.sample(min(len(predictions), 1000), random_state=42)
        fig_pred = px.scatter(
            sample,
            x="actual_price_try",
            y="ml_prediction_try",
            hover_data=["city", "district", "area_m2", "room_layout"],
            title="Actual vs predicted sale prices on test set",
            labels={"actual_price_try": "Actual price, TRY", "ml_prediction_try": "Predicted price, TRY"},
        )
        max_value = float(max(sample["actual_price_try"].max(), sample["ml_prediction_try"].max()))
        fig_pred.add_shape(
            type="line",
            x0=0,
            y0=0,
            x1=max_value,
            y1=max_value,
            line=dict(dash="dash"),
        )
        st.plotly_chart(fig_pred, use_container_width=True)

        residuals = sample.copy()
        residuals["residual_try"] = residuals["actual_price_try"] - residuals["ml_prediction_try"]
        fig_res = px.histogram(
            residuals,
            x="residual_try",
            nbins=60,
            title="Residual distribution",
            labels={"residual_try": "Actual minus predicted price, TRY"},
        )
        st.plotly_chart(fig_res, use_container_width=True)


def affordability_tab(df: pd.DataFrame) -> None:
    """Render simple income-based housing affordability analysis."""
    st.subheader("Affordability analysis")
    st.markdown(
        "This page compares district median sale prices against a user-defined affordability budget. "
        "The budget rule is deliberately simple so it can be explained during the demo."
    )

    annual_income = st.number_input(
        "Annual household income, TRY",
        min_value=0,
        value=1_200_000,
        step=50_000,
        key="affordability_income",
    )
    multiplier = st.slider("Affordable purchase budget multiplier", min_value=2.0, max_value=8.0, value=4.0, step=0.5)
    budget = annual_income * multiplier
    st.metric("Estimated affordable purchase budget", format_try(budget))

    city_options = sorted(df["city"].dropna().unique().tolist())
    city_index = city_options.index("Istanbul") if "Istanbul" in city_options else 0
    city = st.selectbox("City for affordability map", city_options, index=city_index, key="afford_city")
    city_df = df[df["city"] == city]
    district_aff = (
        city_df.groupby("district", as_index=False)
        .agg(
            median_price_try=(TARGET_COLUMN, "median"),
            median_area_m2=("area_m2", "median"),
            listing_count=(TARGET_COLUMN, "size"),
        )
    )
    district_aff["affordability_ratio"] = district_aff["median_price_try"] / budget if budget > 0 else np.nan
    district_aff["affordability_status"] = np.where(
        district_aff["affordability_ratio"] <= 1,
        "Within budget",
        np.where(district_aff["affordability_ratio"] <= 1.5, "Moderately above budget", "Far above budget"),
    )
    district_aff = district_aff.sort_values("affordability_ratio")

    fig = px.bar(
        district_aff,
        x="district",
        y="affordability_ratio",
        color="affordability_status",
        hover_data=["median_price_try", "median_area_m2", "listing_count"],
        title="District affordability ratio based on median sale price",
        labels={"district": "District", "affordability_ratio": "Median price / affordable budget"},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(district_aff, use_container_width=True)


def limitations_tab() -> None:
    """Render limitations and next steps."""
    st.subheader("Limitations and future work")
    st.markdown(
        """
        **Current limitations**

        - The data is based on sale listings, not completed transactions. Asking prices can differ from final sale prices.
        - The model does not include building age, floor level, heating type, parking, elevator or transport proximity because these fields are not available in the current dataset.
        - The dashboard uses a simple affordability rule for demonstration. It does not model credit rates, down payments or household debt.
        - Istanbul has fewer observations than the full national dataset, so the model is trained on all cities and then filtered for Istanbul-oriented analysis.
        - `price_per_m2` is intentionally excluded from model inputs because it is derived from the target and would create data leakage.

        **Potential improvements**

        - Add interest rate and mortgage payment simulation.
        - Add neighborhood-level socioeconomic indicators if a public source is available.
        - Add geocoding and map-based visualization.
        - Compare Random Forest with gradient boosting and regularized linear models.
        - Add model uncertainty through quantile regression or prediction intervals.
        """
    )


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption("DS570 Final Project MVP dashboard")

    if DATA_PATH is None:
        st.error("Processed data was not found. Run src/data/preprocess.py first.")
        st.stop()

    if not ensure_training_artifacts():
        st.stop()

    df = load_data(str(DATA_PATH))
    filtered = filter_dataframe(df)

    model = load_model(str(MODEL_PATH)) if MODEL_PATH is not None else None
    metrics = load_json(str(METRICS_PATH)) if METRICS_PATH is not None else None
    feature_importance = load_csv(str(FEATURE_IMPORTANCE_PATH)) if FEATURE_IMPORTANCE_PATH is not None else None
    predictions = load_csv(str(PREDICTIONS_PATH)) if PREDICTIONS_PATH is not None else None

    tabs = st.tabs(
        [
            "Overview",
            "Exploratory Analysis",
            "Prediction Tool",
            "Model Performance",
            "Affordability",
            "Limitations",
        ]
    )
    with tabs[0]:
        overview_tab(df, filtered)
    with tabs[1]:
        eda_tab(filtered)
    with tabs[2]:
        prediction_tab(df, model)
    with tabs[3]:
        model_performance_tab(metrics, feature_importance, predictions)
    with tabs[4]:
        affordability_tab(df)
    with tabs[5]:
        limitations_tab()


if __name__ == "__main__":
    main()
