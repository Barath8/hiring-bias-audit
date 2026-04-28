# Low Level Design (LLD)

## API Endpoints

### POST /predict
Input: Resume file
Output:
- prediction
- bias_score
- parsed_data

## Internal Flow

1. parse_resume()
2. validate_resume()
3. preprocess()
4. model.predict()
5. gender simulation for bias scoring

## ML Pipeline

- TF-IDF Vectorizer
- RandomForestClassifier
- MLflow logging

## Airflow DAG

- preprocess_data task
- train_model task