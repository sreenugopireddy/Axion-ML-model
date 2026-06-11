from fastapi import APIRouter, HTTPException
from app.schemas import JobStatusResponse, TaskStatus
from app.tasks import celery_app

router = APIRouter(prefix="/api/v1", tags=["jobs"])


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job(job_id: str):
    task = celery_app.AsyncResult(job_id)

    if task.state == "PENDING":
        return JobStatusResponse(job_id=job_id, status=TaskStatus.pending)
    elif task.state == "STARTED":
        return JobStatusResponse(job_id=job_id, status=TaskStatus.running)
    elif task.state == "SUCCESS":
        return JobStatusResponse(job_id=job_id, status=TaskStatus.done, result=task.result)
    elif task.state == "FAILURE":
        return JobStatusResponse(
            job_id=job_id,
            status=TaskStatus.failed,
            error=str(task.info),
        )
    else:
        return JobStatusResponse(job_id=job_id, status=TaskStatus.running)