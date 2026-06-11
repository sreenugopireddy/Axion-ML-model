import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_df():
    np.random.seed(42)
    n = 200
    df = pd.DataFrame({
        "age":    np.random.randint(18, 80, n).astype(float),
        "income": np.random.normal(50000, 15000, n),
        "score":  np.random.uniform(0, 100, n),
        "city":   np.random.choice(["Mumbai", "Delhi", "Bengaluru", None], n),
        "gender": np.random.choice(["M", "F", None], n),
        "target": np.random.randint(0, 2, n),
    })
    rng = np.random.default_rng(42)
    df.loc[rng.choice(n, 20, replace=False), "age"] = np.nan
    df.loc[rng.choice(n, 10, replace=False), "income"] = np.nan
    df.loc[rng.choice(n, 4, replace=False), "income"] = 200000.0
    return df


@pytest.fixture
def clean_numeric_df():
    np.random.seed(0)
    n = 300
    return pd.DataFrame({
        "age":    np.random.randint(20, 60, n).astype(float),
        "income": np.random.normal(60000, 10000, n),
        "score":  np.random.uniform(0, 1, n),
        "target": np.random.randint(0, 2, n),
    })