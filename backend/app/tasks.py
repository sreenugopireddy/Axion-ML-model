from celery import Celery
from app.config import settings
import pandas as pd
import json
import uuid
import io

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


def _get_minio():
    import boto3
    from botocore.client import Config
    return boto3.client(
        "s3",
        endpoint_url=f"http://{settings.minio_endpoint}",
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        config=Config(signature_version="s3v4"),
    )


def _load_df(file_id: str) -> pd.DataFrame:
    s3 = _get_minio()
    obj = s3.get_object(Bucket=settings.minio_bucket, Key=f"{file_id}.csv")
    return pd.read_csv(io.BytesIO(obj["Body"].read()))


def _save_df(df: pd.DataFrame, file_id: str, suffix: str = "cleaned"):
    s3 = _get_minio()
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)
    s3.put_object(
        Bucket=settings.minio_bucket,
        Key=f"{file_id}_{suffix}.csv",
        Body=buf.getvalue(),
    )


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
    from app.pipeline.trainer import Trainer
    import joblib, tempfile, os
    df = _load_df(file_id + "_cleaned")
    trainer = Trainer()
    result, model = trainer.train(df, **params)

    # Save model artifact to MinIO
    with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as f:
        joblib.dump(model, f.name)
        model_path = f.name
    s3 = _get_minio()
    with open(model_path, "rb") as f:
        s3.put_object(
            Bucket=settings.minio_bucket,
            Key=f"{file_id}_model.joblib",
            Body=f.read(),
        )
    os.unlink(model_path)

    return {
        "task": result.task,
        "model_name": result.model_name,
        "cv_score_mean": result.cv_score_mean,
        "cv_score_std": result.cv_score_std,
        "test_score": result.test_score,
        "metric_name": result.metric_name,
        "feature_importances": result.feature_importances,
    }