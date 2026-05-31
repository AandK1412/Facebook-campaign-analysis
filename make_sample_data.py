"""
Generate a synthetic sample dataset so the project runs out of the box.

This produces ``data/sample_data.csv`` with the same schema and roughly the
same shape as the data described in the report: three campaigns (916 = India,
936 = China, 1178 = USA) where the India campaign has the best return on ad
spend and the USA campaign has the highest spend with the worst return.

This is NOT the real Kaggle data — it only exists so the code is runnable.
For real results, download the Kaggle dataset and run ``prepare_data.py``.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

OUT_PATH = "data/sample_data.csv"

# (campaign_id, rows, impressions_scale, conv_rate, roas_mean, spend_scale)
CAMPAIGNS = [
    (916, 50, 1.0e4, 0.0010, 8.0, 1.0),    # India: cheap, high ROAS
    (936, 50, 1.3e4, 0.0009, 6.0, 3.0),    # China: mid
    (1178, 50, 1.7e5, 0.0006, 1.5, 80.0),  # USA: expensive, low ROAS
]

AGE_GROUPS = ["30-34", "35-39", "40-44", "45-49"]
GENDERS = ["M", "F"]


def generate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    ad_id = 100000
    for cid, n, imp_scale, conv_rate, roas_mean, spend_scale in CAMPAIGNS:
        for _ in range(n):
            ad_id += 1
            impressions = max(1, int(rng.exponential(imp_scale)))
            clicks = int(impressions * rng.uniform(0.0005, 0.003))
            spent = round(clicks * rng.uniform(1.0, 2.5) * spend_scale, 2)
            total_conv = int(impressions * conv_rate * rng.uniform(0.5, 1.5))
            approved_conv = int(total_conv * rng.uniform(0.0, 0.6))
            roas = round(max(0.0, rng.normal(roas_mean, roas_mean * 0.4)), 4)
            rows.append(
                {
                    "ad_id": ad_id,
                    "company campaign ID": cid,
                    "facebook campaign ID": rng.integers(100000, 200000),
                    "age": rng.choice(AGE_GROUPS),
                    "gender": rng.choice(GENDERS),
                    "interest": int(rng.integers(2, 115)),
                    "impressions": impressions,
                    "clicks": clicks,
                    "spent": spent,
                    "total conversions": total_conv,
                    "approved conversions": approved_conv,
                    "roas": roas,
                }
            )

    df = pd.DataFrame(rows)
    # Derived metrics (same definitions as data_loader.add_derived_metrics).
    df["click through rate"] = (df["clicks"] / df["impressions"]).fillna(0)
    df["cost per click"] = (
        (df["spent"] / df["clicks"]).replace([np.inf, -np.inf], 0).fillna(0)
    )
    df["cost per conversion"] = (
        (df["spent"] / df["total conversions"]).replace([np.inf, -np.inf], 0).fillna(0)
    )
    return df


def main() -> None:
    df = generate()
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(df)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
