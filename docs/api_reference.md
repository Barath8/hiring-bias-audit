# API Reference

## POST /predict

### Input
- file: PDF resume

### Output
```json
{
  "prediction": 1,
  "bias_score": 0.23,
  "bias_flag": true
}