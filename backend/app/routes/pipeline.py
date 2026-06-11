from fastapi import APIRouter, HTTPException
from app.schemas import CleanRequest, CleanResponse, EDARequest, EDAResponse, TaskStatus
from app.tasks import run_clean, run_eda

router = APIRouter(prefix="/api/v1", tags=["pipeline"])


@router.post("/clean", response_model=CleanResponse)
async def clean(req: CleanRequest):
    task = run_clean.delay(
        req.file_id,
        {
            "impute_numeric": req.impute_numeric,
            "impute_categorical": req.impute_categorical,
            "outlier_method": req.outlier_method,
            "outlier_threshold": req.outlier_threshold,
            "drop_duplicates": req.drop_duplicates,
        },
    )
    return CleanResponse(
        job_id=task.id,
        status=TaskStatus.pending,
        message="Clean job queued",
    )


@router.post("/eda", response_model=EDAResponse)
async def eda(req: EDARequest):
    task = run_eda.delay(req.file_id)
    return EDAResponse(
        job_id=task.id,
        status=TaskStatus.pending,
        message="EDA job queued",
    )