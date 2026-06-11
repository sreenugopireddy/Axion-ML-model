from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, pipeline, train, jobs

app = FastAPI(
    title="Axon API",
    description="ML pipeline platform — clean, transform, analyse, train",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(pipeline.router)
app.include_router(train.router)
app.include_router(jobs.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "axon-api"}