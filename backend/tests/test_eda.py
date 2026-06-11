from app.pipeline.eda import EDA
from app.pipeline.cleaner import Cleaner


def test_describe_has_numeric_cols(sample_df):
    eda = EDA()
    cleaner = Cleaner()
    df, _ = cleaner.clean(sample_df)
    result = eda.analyse(df)
    assert "age" in result.describe
    assert "income" in result.describe


def test_null_pct_zero_after_clean(sample_df):
    cleaner = Cleaner()
    df, _ = cleaner.clean(sample_df)
    eda = EDA()
    result = eda.analyse(df)
    assert all(v == 0.0 for v in result.null_pct.values())


def test_correlation_symmetric(sample_df):
    cleaner = Cleaner()
    df, _ = cleaner.clean(sample_df)
    eda = EDA()
    result = eda.analyse(df)
    corr = result.correlation
    for col_a, row in corr.items():
        for col_b, val in row.items():
            assert abs(val - corr[col_b][col_a]) < 1e-9