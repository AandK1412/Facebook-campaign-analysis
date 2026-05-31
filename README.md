# Business Advertisement Expense Minimization

Minimize advertising spend across marketing campaigns using **Linear
Programming**, with supporting exploratory analysis and visualization.

Given a company running ad campaigns in several regions, the model decides how
much to invest in each campaign so that **total cost is minimized** while still
meeting minimum targets for impressions, clicks and conversions. It uses
[PuLP](https://coin-or.github.io/pulp/) to formulate and solve the LP and
[pandas](https://pandas.pydata.org/) / [matplotlib](https://matplotlib.org/) /
[seaborn](https://seaborn.pydata.org/) for analysis and charts.

This is a cleaned-up, runnable version of an academic mini-project (NMIMS /
MPSTME, 2022–23) by Anrunya Patole, Kshama Purohit and Archita Rai.

## The optimization model

```
minimize    Σ_c  mean_spent[c] · x_c
subject to  Σ_c  mean_metric[c, m] · x_c  ≥  target[m]   for each metric m
            x_c ≥ 0,  integer
```

- `c` ranges over campaign IDs (`916`, `936`, `1178`)
- `m` ranges over metrics (`impressions`, `clicks`, `total conversions`)
- `x_c` is the recommended number of advertising "units" to buy under campaign `c`
- coefficients are the **per-campaign averages** computed from the dataset

## Quick start

```bash
# 1. Install dependencies (a virtual environment is recommended)
pip install -r requirements.txt

# 2. Generate a synthetic dataset so the code runs out of the box
python make_sample_data.py

# 3. Solve the model with the example targets from the report
python -m src.main --data data/sample_data.csv \
    --impressions 150000 --clicks 50 --conversions 10

# ...or run interactively (prompts you for each target)
python -m src.main --data data/sample_data.csv

# Generate all analysis figures into figures/
python -m src.main --data data/sample_data.csv \
    --impressions 150000 --clicks 50 --conversions 10 --plots
```

Example output:

```
Solver status : Optimal
Minimum cost  : 481.49 (units)
Allocation:
  campaign 916: 16
  campaign 936: 0
  campaign 1178: 0
```

The optimizer concentrates spend on campaign **916** — the highest
return-on-ad-spend campaign — which matches the report's finding.

## Using the real data

The analysis is built around the public Kaggle
[Sales Conversion Optimization](https://www.kaggle.com/datasets/loveall/clicks-conversion-tracking)
dataset. Once downloaded:

```bash
python prepare_data.py path/to/KAG_conversion_data.csv
```

See [`data/README.md`](data/README.md) for the expected schema and details on
how ROAS is estimated.

## Project layout

```
.
├── src/
│   ├── optimizer.py      # builds and solves the linear program
│   ├── data_loader.py    # loading, validation, derived metrics, Kaggle mapping
│   ├── visualize.py      # the exploratory charts from the report
│   └── main.py           # command-line entry point
├── make_sample_data.py   # generate a synthetic dataset (runs offline)
├── prepare_data.py       # convert the raw Kaggle CSV to the project schema
├── data/                 # dataset lives here
├── figures/              # generated charts (created on first --plots run)
├── docs/                 # original report notes
├── requirements.txt
├── LICENSE
└── README.md
```

## Use as a library

```python
from src import data_loader, optimizer

df = data_loader.load("data/sample_data.csv")
result = optimizer.solve(
    df,
    targets={"impressions": 150000, "clicks": 50, "total conversions": 10},
)
print(result.status, result.objective, result.allocation)
```

## Notes

- `make_sample_data.py` produces **synthetic** data purely so the project runs
  without the Kaggle download. Results from it are illustrative only.
- The raw Kaggle data has no revenue field, so ROAS is *estimated*; adjust the
  assumption via `prepare_data.py --value-per-conversion`.

## License

MIT — see [LICENSE](LICENSE).
