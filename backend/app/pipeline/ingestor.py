import pandas as pd
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Union


@dataclass
class DatasetMeta:
    rows: int
    cols: int
    columns: list
    dtypes: dict
    null_counts: dict
    numeric_cols: list
    categorical_cols: list
    memory_mb: float


class Ingestor:
    SUPPORTED = {".csv", ".parquet", ".tsv"}

    def load(self, source: Union[str, Path]) -> tuple:
        path = Path(source)
        if path.suffix not in self.SUPPORTED:
            raise ValueError(f"Unsupported format: {path.suffix}. Use {self.SUPPORTED}")
        if path.suffix == ".parquet":
            df = pd.read_parquet(path)
        elif path.suffix == ".tsv":
            df = pd.read_csv(path, sep="\t")
        else:
            df = pd.read_csv(path)
        df = self._coerce_dtypes(df)
        return df, self._build_meta(df)

    def load_bytes(self, data: bytes, filename: str) -> tuple:
        import io
        suffix = Path(filename).suffix
        if suffix == ".parquet":
            df = pd.read_parquet(io.BytesIO(data))
        elif suffix == ".tsv":
            df = pd.read_csv(io.BytesIO(data), sep="\t")
        else:
            df = pd.read_csv(io.BytesIO(data))
        df = self._coerce_dtypes(df)
        return df, self._build_meta(df)

    def _coerce_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.select_dtypes(include="object").columns:
            coerced = pd.to_numeric(df[col], errors="coerce")
            if coerced.notna().sum() / len(df) > 0.85:
                df[col] = coerced
        return df

    def _build_meta(self, df: pd.DataFrame) -> DatasetMeta:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        return DatasetMeta(
            rows=len(df),
            cols=len(df.columns),
            columns=df.columns.tolist(),
            dtypes={c: str(df[c].dtype) for c in df.columns},
            null_counts={c: int(df[c].isna().sum()) for c in df.columns},
            numeric_cols=numeric_cols,
            categorical_cols=categorical_cols,
            memory_mb=round(df.memory_usage(deep=True).sum() / 1e6, 3),
        )