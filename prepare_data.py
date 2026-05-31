"""
Convert the raw Kaggle dataset into the schema this project expects.

Usage:
    python prepare_data.py path/to/KAG_conversion_data.csv

Writes ``data/sample_data.csv``. Optionally set the assumed revenue per
approved conversion (used only to estimate ROAS, which the raw data lacks):

    python prepare_data.py KAG_conversion_data.csv --value-per-conversion 5
"""

from __future__ import annotations

import argparse

from src import data_loader


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("raw_csv", help="Path to the raw Kaggle conversion CSV.")
    p.add_argument(
        "--value-per-conversion",
        type=float,
        default=5.0,
        help="Assumed revenue per approved conversion, for the ROAS estimate.",
    )
    p.add_argument("--out", default="data/sample_data.csv")
    args = p.parse_args()

    df = data_loader.from_kaggle_raw(args.raw_csv, args.value_per_conversion)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
