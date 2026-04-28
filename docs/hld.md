# High Level Design (HLD)

## Goal
Detect hiring bias in resume screening using ML + MLOps pipeline.

## Architecture Style
Microservice-based MLOps system

## Modules

### 1. Frontend
- Upload resumes
- Display prediction + bias score

### 2. Backend (FastAPI)
- Parse resume
- Preprocess text
- Predict hiring outcome
- Compute bias score

### 3. ML Pipeline
- TF-IDF Vectorization
- RandomForest model
- MLflow tracking

### 4. Orchestration (Airflow)
- Scheduled retraining pipeline
- DAG-based execution

### 5. Monitoring
- Prometheus collects metrics
- Grafana visualizes bias trends