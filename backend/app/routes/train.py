from fastapi import APIRouter
from app.schemas import TrainRequest, TrainResponse, TaskStatus
from app.tasks import run_train

router = APIRouter(prefix="/api/v1", tags=["train"])


@router.post("/train", response_model=TrainResponse)
async def train(req: TrainRequest):
    task = run_train.delay(
        req.file_id,
        {
            "target": req.target,
            "task": req.task,
            "model_name": req.model_name,
            "test_size": req.test_size,
        },
    )
    return TrainResponse(
        job_id=task.id,
        status=TaskStatus.pending,
        message="Train job queued",
    )