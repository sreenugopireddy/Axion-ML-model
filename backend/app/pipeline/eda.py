import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EDAResult:
    describe: dict[str, Any]           # df.describe() as dict
    null_pct: dict[str, float]         # % nulls per column
    correlation: dict[str, Any]        # correlation matrix as dict
    top_value_counts: dict[str, Any]   # top 10 value counts for categoricals
    skewness: dict[str, float]         # skewness for numeric cols
    outlier_flags: dict[str, int]      # IQR outlier count per numeric col


class EDA:
    """
    Descriptive stats, correlation, distribution analysis.
    Returns JSON-serializable dicts — ready to pass to FastAPI in Phase 2.
    """

    def analyse(self, df: pd.DataFrame) -> EDAResult:
        numeric = df.select_dtypes(include=np.number)
        categorical = df.select_dtypes(exclude=np.number)

        return EDAResult(
            describe=numeric.describe().round(4).to_dict(),
            null_pct={col: round(df[col].isna().mean() * 100, 2) for col in df.columns},
            correlation=numeric.corr().round(4).to_dict() if not numeric.empty else {},
            top_value_counts={
                col: df[col].value_counts().head(10).to_dict()
                for col in categorical.columns
            },
            skewness={
                col: round(float(df[col].skew()), 4)
                for col in numeric.columns
            },
            outlier_flags=self._flag_outliers(numeric),
        )

    def _flag_outliers(self, numeric: pd.DataFrame) -> dict[str, int]:
        flags = {}
        for col in numeric.columns:
            q1, q3 = numeric[col].quantile(0.25), numeric[col].quantile(0.75)
            iqr = q3 - q1
            n_out = int(((numeric[col] < q1 - 1.5 * iqr) | (numeric[col] > q3 + 1.5 * iqr)).sum())
            if n_out > 0:
                flags[col] = n_out
        return flags