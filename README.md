# Axon — ML Pipeline Studio

> Upload any dataset. Clean it. Analyse it. Train a model. All from your browser.

[![Tests](https://github.com/sreenugopireddy/Axion-ML-model/actions/workflows/deploy.yml/badge.svg)](https://github.com/sreenugopireddy/Axion-ML-model/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue?logo=react)](https://react.dev)
[![Celery](https://img.shields.io/badge/Celery-5.3-brightgreen?logo=celery)](https://docs.celeryq.dev)
[![Railway](https://img.shields.io/badge/Backend-Railway-purple?logo=railway)](https://axios-production-4a48.up.railway.app)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://axon-pi-two.vercel.app)

---

## Live Demo

| | URL |
|---|---|
| **Frontend** | https://axon-pi-two.vercel.app |
| **API** | https://axios-production-4a48.up.railway.app |
| **API Docs** | https://axios-production-4a48.up.railway.app/docs |

---

## What is Axon?

Axon is a production-grade ML pipeline platform that turns raw CSV data into cleaned, analysed, and model-ready datasets — through a REST API and a React frontend. No code required for the end user.

Built in 4 phases over a week:

- **Phase 1** — Pure Python pipeline modules with 87% test coverage
- **Phase 2** — FastAPI async job system with Celery + Redis
- **Phase 3** — React + Vite + TailwindCSS frontend
- **Phase 4** — Docker + Railway + Vercel + GitHub Actions CI/CD

---

## Features

- **CSV / TSV / Parquet ingestion** — upload any tabular file, auto-infer column types
- **Data cleaning** — null imputation (mean / median / mode / constant / drop), IQR and Z-score outlier removal, duplicate detection
- **EDA** — descriptive stats, correlation matrix, skewness, outlier flags, value counts
- **Model training** — Random Forest, Logistic Regression, Gradient Boosting via sklearn pipelines with cross-validation and feature importances
- **Async jobs** — every pipeline run is a Celery task; poll `/jobs/{id}` for status
- **REST API** — full OpenAPI spec, use from any language or tool

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React + Vite (Vercel)               │
│          Upload → Overview → Clean → Results         │
└────────────────────────┬────────────────────────────┘
                         │ REST
┌────────────────────────▼────────────────────────────┐
│              FastAPI (Railway)                       │
│   /upload  /clean  /eda  /train  /jobs/{id}         │
└──────┬─────────────────┬───────────────────┬────────┘
       │                 │                   │
┌──────▼──────┐  ┌───────▼──────┐  ┌────────▼───────┐
│   Celery    │  │    Redis     │  │   /tmp storage  │
│   Worker   │  │   Broker     │  │   (file cache)  │
└──────┬──────┘  └──────────────┘  └────────────────┘
       │
┌──────▼────────────────────────────────────────────┐
│              Pipeline Modules                      │
│  ingestor → cleaner → transformer → eda → trainer │
└───────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
| Tool | Purpose |
|---|---|
| FastAPI | REST API framework |
| Celery | Async task queue |
| Redis | Message broker + result backend |
| pandas / numpy | Data processing |
| scikit-learn | ML models and pipelines |
| XGBoost / LightGBM | Gradient boosting |
| SHAP | Feature explainability |
| pytest + pytest-cov | Testing (87% coverage) |

### Frontend
| Tool | Purpose |
|---|---|
| React 18 + Vite | UI framework |
| TypeScript | Type safety |
| TailwindCSS | Styling |
| Axios | API client |

### Infrastructure
| Tool | Purpose |
|---|---|
| Railway | Backend hosting |
| Vercel | Frontend hosting |
| GitHub Actions | CI/CD pipeline |
| Docker | Containerisation |

---

## Project Structure

```
axon/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings (pydantic-settings)
│   │   ├── schemas.py           # Pydantic request/response models
│   │   ├── tasks.py             # Celery async tasks
│   │   ├── routes/
│   │   │   ├── upload.py        # POST /api/v1/upload
│   │   │   ├── pipeline.py      # POST /api/v1/clean, /eda
│   │   │   ├── train.py         # POST /api/v1/train
│   │   │   └── jobs.py          # GET /api/v1/jobs/{id}
│   │   └── pipeline/
│   │       ├── ingestor.py      # CSV/TSV/Parquet loader
│   │       ├── cleaner.py       # Null imputation + outlier removal
│   │       ├── transformer.py   # Scaling + encoding
│   │       ├── eda.py           # Statistical analysis
│   │       └── trainer.py       # sklearn model training
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_ingestor.py
│   │   ├── test_cleaner.py
│   │   └── test_eda.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.ts
│   │   │   ├── types.ts
│   │   │   ├── useUpload.ts
│   │   │   └── useJob.ts
│   │   └── components/
│   │       ├── FileUpload.tsx
│   │       ├── DatasetOverview.tsx
│   │       └── JobResult.tsx
│   └── package.json
├── infra/
│   └── docker-compose.yml
└── .github/
    └── workflows/
        └── deploy.yml
```

---

## API Reference

### Upload a dataset
```bash
POST /api/v1/upload
Content-Type: multipart/form-data

curl -X POST https://axios-production-4a48.up.railway.app/api/v1/upload \
  -F "file=@your_data.csv"
```

Response:
```json
{
  "file_id": "314ce166-...",
  "filename": "your_data.csv",
  "rows": 1111,
  "cols": 529,
  "numeric_cols": [...],
  "categorical_cols": [...],
  "null_counts": {...},
  "memory_mb": 4.702
}
```

### Run clean pipeline
```bash
POST /api/v1/clean
Content-Type: application/json

{
  "file_id": "314ce166-...",
  "impute_numeric": "median",
  "impute_categorical": "mode",
  "outlier_method": "iqr",
  "outlier_threshold": 1.5,
  "drop_duplicates": true
}
```

### Poll job status
```bash
GET /api/v1/jobs/{job_id}
```

Response:
```json
{
  "job_id": "9ea15b6e-...",
  "status": "done",
  "result": {
    "rows_before": 1111,
    "rows_after": 1110,
    "rows_dropped": 1,
    "duplicates_removed": 1,
    "nulls_filled": {},
    "outliers_removed": {}
  }
}
```

---

## Run Locally

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker Desktop

### Backend

```bash
git clone https://github.com/sreenugopireddy/Axion-ML-model.git
cd Axion-ML-model/backend
pip install -r requirements.txt

# Start Redis + MinIO
cd ../infra
docker-compose up redis minio -d

# Start FastAPI
cd ../backend
uvicorn app.main:app --reload --port 8000

# Start Celery worker (new terminal)
python -m celery -A app.tasks.celery_app worker --loglevel=info --pool=solo
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

### Run Tests

```bash
cd backend
python -m pytest tests/ -v --cov=app/pipeline --cov-report=term-missing
```

```
13 passed, 87% coverage
```

---

## CI/CD Pipeline

Every push to `main` triggers:

```
push to main
    │
    ▼
run pytest (13 tests)
    │
    ├──► deploy backend → Railway (auto on test pass)
    │
    └──► build React → deploy → Vercel
```

---

## What I Learned Building This

- Designing async ML pipelines with Celery task queues
- Production FastAPI patterns — Pydantic schemas, dependency injection, CORS
- React polling patterns for long-running jobs
- Docker + Railway deployment with root directory configuration
- GitHub Actions CI/CD with multi-job dependency chains
- Why pandas `inplace=True` on slices breaks in pandas 3.0

---

## Author

**Sreenu Gopireddy**
B.Tech Data Science, Santhiram Engineering College (2023-2027)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/sreenugopireddy)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/sreenugopireddy)

---

## Roadmap

- [ ] AI chat assistant powered by Llama 3.1 70B (Groq)
- [ ] Auto EDA report generation
- [ ] EDA charts (correlation heatmap, distributions)
- [ ] HuggingFace Spaces deployment
- [ ] Python SDK (`pip install axon-sdk`)

---

*Built from scratch in 4 phases — local Python modules → FastAPI → React → cloud deploy.*
