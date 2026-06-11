from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import UploadResponse
from app.pipeline.ingestor import Ingestor
from app.config import settings
import uuid
import io
import boto3
from botocore.client import Config

router = APIRouter(prefix="/api/v1", tags=["upload"])


def get_s3():
    return boto3.client(
        "s3",
        endpoint_url=f"http://{settings.minio_endpoint}",
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        config=Config(signature_version="s3v4"),
    )


def ensure_bucket(s3):
    try:
        s3.head_bucket(Bucket=settings.minio_bucket)
    except Exception:
        s3.create_bucket(Bucket=settings.minio_bucket)


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".tsv", ".parquet")):
        raise HTTPException(400, "Only CSV, TSV, and Parquet files supported")

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(400, "Uploaded file is empty")

    ingestor = Ingestor()
    try:
        df, meta = ingestor.load_bytes(data, file.filename)
    except Exception as e:
        raise HTTPException(422, f"Could not parse file: {str(e)}")

    file_id = str(uuid.uuid4())

    s3 = get_s3()
    ensure_bucket(s3)
    s3.put_object(
        Bucket=settings.minio_bucket,
        Key=f"{file_id}.csv",
        Body=data,
    )

    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        rows=meta.rows,
        cols=meta.cols,
        columns=meta.columns,
        numeric_cols=meta.numeric_cols,
        categorical_cols=meta.categorical_cols,
        null_counts=meta.null_counts,
        memory_mb=meta.memory_mb,
    )