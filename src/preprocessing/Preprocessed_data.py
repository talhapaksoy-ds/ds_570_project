"""
Preprocess Turkish house sales data for the DS570 final project.

Input:
    data/raw/processed_turkish_house_sales.csv

Outputs:
    data/processed/house_sales_cleaned_for_ds570.csv
    data/processed/istanbul_house_sales_subset_for_ds570.csv
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd


TURKISH_MONTHS = {
    "Ocak": 1,
    "Şubat": 2,
    "Subat": 2,
    "Mart": 3,
    "Nisan": 4,
    "Mayıs": 5,
    "Mayis": 5,
    "Haziran": 6,
    "Temmuz": 7,
    "Ağustos": 8,
    "Agustos": 8,
    "Eylül": 9,
    "Eylul": 9,
    "Ekim": 10,
    "Kasım": 11,
    "Kasim": 11,
    "Aralık": 12,
    "Aralik": 12,
}


def parse_room_layout(value: object) -> pd.Series:
    """Parse room layout strings such as '3+1', '3.5+1', 'Stüdyo (1+0)'."""
    text = str(value).strip()

    if "Stüdyo" in text or "Studyo" in text or "1+0" in text:
        return pd.Series({"rooms": 1.0, "living_rooms": 0.0, "total_rooms": 1.0})

    if "10 Üzeri" in text or "10 Uzeri" in text:
        return pd.Series({"rooms": 10.0, "living_rooms": 0.0, "total_rooms": 10.0})

    match = re.match(r"^\s*(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)\s*$", text)
    if match:
        rooms = float(match.group(1))
        living_rooms = float(match.group(2))
        return pd.Series(
            {
                "rooms": rooms,
                "living_rooms": living_rooms,
                "total_rooms": rooms + living_rooms,
            }
        )

    return pd.Series({"rooms": np.nan, "living_rooms": np.nan, "total_rooms": np.nan})


def parse_turkish_date(value: object) -> pd.Timestamp:
    """Parse dates such as '25 Mayıs  2025'."""
    text = str(value).strip()
    parts = text.split()

    if len(parts) >= 3:
        day = int(parts[0])
        month = TURKISH_MONTHS.get(parts[1])
        year = int(parts[2])

        if month is not None:
            return pd.Timestamp(year=year, month=month, day=day)

    return pd.NaT


def preprocess(input_path: str | Path, output_dir: str | Path) -> pd.DataFrame:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(input_path, encoding="utf-8-sig")

    data = raw.rename(
        columns={
            "satici_tip": "seller_type",
            "Metrekare": "area_m2",
            "Oda_Sayisi": "room_layout",
            "il": "city",
            "Ilce": "district",
            "Mahalle": "neighborhood",
            "Tarih": "listing_date_raw",
            "fiyat": "price_try",
        }
    ).copy()

    parsed_rooms = data["room_layout"].apply(parse_room_layout)
    data = pd.concat([data, parsed_rooms], axis=1)

    data["listing_date"] = data["listing_date_raw"].apply(parse_turkish_date)
    data["listing_month"] = data["listing_date"].dt.month
    data["listing_day"] = data["listing_date"].dt.day
    data["price_per_m2"] = data["price_try"] / data["area_m2"]

    domain_mask = (
        data["area_m2"].between(20, 500)
        & data["price_try"].between(500_000, 50_000_000)
        & data["rooms"].notna()
    )

    price_low, price_high = data["price_try"].quantile([0.01, 0.99])
    area_low, area_high = data["area_m2"].quantile([0.01, 0.99])
    percentile_mask = (
        data["area_m2"].between(area_low, area_high)
        & data["price_try"].between(price_low, price_high)
        & data["rooms"].notna()
    )

    data["is_model_candidate_domain"] = domain_mask
    data["is_model_candidate_pct"] = percentile_mask

    data.to_csv(output_dir / "house_sales_cleaned_for_ds570.csv", index=False, encoding="utf-8-sig")
    data[data["city"].eq("Istanbul")].to_csv(
        output_dir / "istanbul_house_sales_subset_for_ds570.csv",
        index=False,
        encoding="utf-8-sig",
    )

    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/raw/processed_turkish_house_sales.csv",
        help="Path to the raw CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed",
        help="Directory where processed files will be written.",
    )
    args = parser.parse_args()

    data = preprocess(args.input, args.output_dir)
    print(f"Preprocessing completed. Rows: {len(data):,}, Columns: {len(data.columns):,}")


if __name__ == "__main__":
    main()

