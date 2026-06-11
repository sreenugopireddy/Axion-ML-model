import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Literal

ImputeStrategy = Literal["mean", "median", "mode", "constant", "drop"]
OutlierMethod = Literal["iqr", "zscore", "none"]


@dataclass
class CleanReport:
    rows_before: int
    rows_after: int
    rows_dropped: int
    nulls_filled: dict
    outliers_removed: dict
    duplicates_removed: int


class Cleaner:
    def clean(
        self,
        df: pd.DataFrame,
        impute_numeric: ImputeStrategy = "median",
        impute_categorical: ImputeStrategy = "mode",
        outlier_method: OutlierMethod = "iqr",
        outlier_threshold: float = 1.5,
        drop_duplicates: bool = True,
        constant_fill: dict = None,
    ) -> tuple:
        df = df.copy()
        report = CleanReport(
            rows_before=len(df),
            rows_after=0,
            rows_dropped=0,
            nulls_filled={},
            outliers_removed={},
            duplicates_removed=0,
        )

        if drop_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            report.duplicates_removed = before - len(df)

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

        for col in numeric_cols:
            n_null = int(df[col].isna().sum())
            if n_null == 0:
                continue
            if impute_numeric == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif impute_numeric == "median":
                df[col] = df[col].fillna(df[col].median())
            elif impute_numeric == "mode":
                df[col] = df[col].fillna(df[col].mode()[0])
            elif impute_numeric == "constant":
                df[col] = df[col].fillna((constant_fill or {}).get(col, 0))
            elif impute_numeric == "drop":
                df = df.dropna(subset=[col])
            report.nulls_filled[col] = n_null

        for col in cat_cols:
            n_null = int(df[col].isna().sum())
            if n_null == 0:
                continue
            if impute_categorical == "mode":
                fill_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                df[col] = df[col].fillna(fill_val)
            elif impute_categorical == "constant":
                df[col] = df[col].fillna((constant_fill or {}).get(col, "Unknown"))
            elif impute_categorical == "drop":
                df = df.dropna(subset=[col])
            report.nulls_filled[col] = n_null

        if outlier_method != "none":
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            for col in numeric_cols:
                before = len(df)
                if outlier_method == "iqr":
                    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
                    iqr = q3 - q1
                    df = df[
                        (df[col] >= q1 - outlier_threshold * iqr) &
                        (df[col] <= q3 + outlier_threshold * iqr)
                    ]
                elif outlier_method == "zscore":
                    z = np.abs((df[col] - df[col].mean()) / df[col].std())
                    df = df[z < outlier_threshold]
                removed = before - len(df)
                if removed > 0:
                    report.outliers_removed[col] = removed

        report.rows_after = len(df)
        report.rows_dropped = report.rows_before - report.rows_after
        return df.reset_index(drop=True), report