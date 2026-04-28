# Test Plan

## Unit Tests
- Resume parser validation
- Preprocessing correctness
- Model prediction output

## Integration Tests
- API endpoint /predict
- MLflow logging validation
- Airflow DAG execution

## Performance Tests
- API latency < 300ms
- Batch training execution time

## Bias Tests
- Male vs Female prediction difference
- Bias threshold validation (>0.2 flagged)