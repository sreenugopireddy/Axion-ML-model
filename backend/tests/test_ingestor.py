import pytest
from app.pipeline.ingestor import Ingestor


def test_load_csv(tmp_path):
    csv = tmp_path / "test.csv"
    csv.write_text("age,income,city\n25,50000,Delhi\n30,60000,Mumbai\n")
    ing = Ingestor()
    df, meta = ing.load(csv)
    assert meta.rows == 2
    assert meta.cols == 3
    assert "age" in meta.numeric_cols
    assert "city" in meta.categorical_cols


def test_load_bytes():
    raw = b"age,score\n22,88.5\n35,92.0\n"
    ing = Ingestor()
    df, meta = ing.load_bytes(raw, "data.csv")
    assert meta.rows == 2
    assert meta.null_counts == {"age": 0, "score": 0}


def test_unsupported_format(tmp_path):
    f = tmp_path / "data.xlsx"
    f.write_bytes(b"fake")
    ing = Ingestor()
    with pytest.raises(ValueError, match="Unsupported format"):
        ing.load(f)


def test_null_detection():
    raw = b"age,income\n25,\n,60000\n30,55000\n"
    ing = Ingestor()
    df, meta = ing.load_bytes(raw, "data.csv")
    assert meta.null_counts["income"] >= 1
    assert meta.null_counts["age"] >= 1