from celery import Celery
from app.config import settings
import os

celery_app = Celery(
    "axon",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)

UPLOAD_DIR = "/tmp/axon_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _load_df(file_id: str):
    import pandas as pd
    path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    return pd.read_csv(path)


def _save_df(df, file_id: str, suffix: str = "cleaned"):
    path = os.path.join(UPLOAD_DIR, f"{file_id}_{suffix}.csv")
    df.to_csv(path, index=False)


@celery_app.task(bind=True)
def run_clean(self, file_id: str, params: dict):
    from app.pipeline.cleaner import Cleaner
    df = _load_df(file_id)
    cleaner = Cleaner()
    df_clean, report = cleaner.clean(df, **params)
    _save_df(df_clean, file_id, suffix="cleaned")
    return {
        "rows_before": report.rows_before,
        "rows_after": report.rows_after,
        "rows_dropped": report.rows_dropped,
        "duplicates_removed": report.duplicates_removed,
        "nulls_filled": report.nulls_filled,
        "outliers_removed": report.outliers_removed,
    }


@celery_app.task(bind=True)
def run_eda(self, file_id: str):
    from app.pipeline.eda import EDA
    df = _load_df(file_id)
    eda = EDA()
    result = eda.analyse(df)
    return {
        "describe": result.describe,
        "null_pct": result.null_pct,
        "correlation": result.correlation,
        "top_value_counts": result.top_value_counts,
        "skewness": result.skewness,
        "outlier_flags": result.outlier_flags,
    }


@celery_app.task(bind=True)
def run_train(self, file_id: str, params: dict):
    import joblib
    from app.pipeline.trainer import Trainer
    df = _load_df(file_id + "_cleaned")
    trainer = Trainer()
    result, model = trainer.train(df, **params)
    model_path = os.path.join(UPLOAD_DIR, f"{file_id}_model.joblib")
    joblib.dump(model, model_path)
    return {
        "task": result.task,
        "model_name": result.model_name,
        "cv_score_mean": result.cv_score_mean,
        "cv_score_std": result.cv_score_std,
        "test_score": result.test_score,
        "metric_name": result.metric_name,
        "feature_importances": result.feature_importances,
    }
