from app.pipeline.cleaner import Cleaner


def test_removes_nulls(sample_df):
    cleaner = Cleaner()
    df_clean, report = cleaner.clean(sample_df)
    assert df_clean.isnull().sum().sum() == 0


def test_nulls_filled_recorded(sample_df):
    cleaner = Cleaner()
    _, report = cleaner.clean(sample_df)
    assert len(report.nulls_filled) > 0


def test_iqr_outlier_removal(sample_df):
    cleaner = Cleaner()
    df_clean, report = cleaner.clean(sample_df, outlier_method="iqr")
    assert df_clean["income"].max() < 200000


def test_row_count_after_clean(sample_df):
    cleaner = Cleaner()
    df_clean, report = cleaner.clean(sample_df)
    assert len(df_clean) <= len(sample_df)


def test_report_totals(sample_df):
    cleaner = Cleaner()
    df_clean, report = cleaner.clean(sample_df)
    assert report.rows_after == len(df_clean)
    assert report.rows_dropped == report.rows_before - report.rows_after


def test_zscore_method(sample_df):
    cleaner = Cleaner()
    df_clean, report = cleaner.clean(sample_df, outlier_method="zscore", outlier_threshold=3.0)
    assert df_clean.isnull().sum().sum() == 0