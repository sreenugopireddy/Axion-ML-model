from pydantic import BaseModel
from typing import Any, Optional
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    rows: int
    cols: int
    columns: list[str]
    numeric_cols: list[str]
    categorical_cols: list[str]
    null_counts: dict[str, int]
    memory_mb: float


class CleanRequest(BaseModel):
    file_id: str
    impute_numeric: str = "median"
    impute_categorical: str = "mode"
    outlier_method: str = "iqr"
    outlier_threshold: float = 1.5
    drop_duplicates: bool = True


class CleanResponse(BaseModel):
    job_id: str
    status: TaskStatus
    message: str


class EDARequest(BaseModel):
    file_id: str


class EDAResponse(BaseModel):
    job_id: str
    status: TaskStatus
    message: str


class TrainRequest(BaseModel):
    file_id: str
    target: str
    task: str = "classification"
    model_name: str = "random_forest"
    test_size: float = 0.2


class TrainResponse(BaseModel):
    job_id: str
    status: TaskStatus
    message: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: TaskStatus
    result: Optional[Any] = None
    error: Optional[str] = None
class TrainRequest(BaseModel):
    model_config = {"protected_namespaces": ()}  # add this line
    file_id: str
    target: str
    task: str = "classification"
    model_name: str = "random_forest"
    test_size: float = 0.2