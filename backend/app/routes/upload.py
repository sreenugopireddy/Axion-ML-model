from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas import UploadResponse
from app.pipeline.ingestor import Ingestor
import uuid
import os

router = APIRouter(prefix="/api/v1", tags=["upload"])

UPLOAD_DIR = "/tmp/axon_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
    path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    with open(path, "wb") as f:
        f.write(data)
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
