# Gas Distribution Analytics

Data engineering + analytics + ML pipeline for city gas distribution (CGD) operational insights.

## Project structure

- `data/raw/` - raw source dataset(s)
- `data/processed/` - cleaned and transformed outputs
- `data/analytics_outputs/` - precomputed analytics artifacts
- `src/cleaning/` - cleaning utility functions
- `src/transformations/` - feature engineering and transformation functions
- `src/analytics/` - analytics aggregation and export functions
- `src/ml/` - machine learning models for leak detection and demand forecasting
- `src/ingestion/` - ingestion abstraction helpers
- `pipelines/` - executable pipeline scripts
- `tests/` - pytest suite
- `notebooks/` - exploratory notebooks including cleaning and visualization

## Quick start

1. Clone repository

```bash
git clone https://github.com/alloy77/Gas-Distribution_Analytics.git 
cd Gas-Distribution_Analytics
```

2. Create virtual environment

```bash
python -m venv .gas
. .gas/Scripts/Activate.ps1
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run relevant pipeline(s)

```bash
python -m pipelines.raw_data_watcher
# or individually:
python -m pipelines.cleaning_pipeline
python -m pipelines.transformation_pipeline
python -m pipelines.analytics_pipeline
python -m pipelines.ml_pipeline
```

## Testing

```bash
pytest -q --junitxml=tests/reports/results.xml
```

## Notebook visualizations

- `notebooks/04_analytics_visualization.ipynb` includes:
  - hourly demand trend
  - zone consumption comparison
  - UFG loss chart
  - pressure violation counts
  - leak hotspot map
  - demand forecast

- `notebooks/Cleaning_notebook.ipynb` shows step-by-step cleaning processes

## CI (Jenkins)

`Jenkinsfile` pipeline:
- install dependencies
- run pytest
- run pipelines through `pipelines/raw_data_watcher.py`

## Data flow

1. New `data/raw/CGD_Raw.csv` ingestion
2. cleaning pipeline -> `data/processed/CGD_Transformation_Final.csv`
3. transformation pipeline -> various processed artifacts
4. analytics pipeline -> `data/analytics_outputs/..`
5. ML pipeline -> model training and forecasting

## Notes

- Replace sample dataset and paths with actual company data where applicable
- For `--html` report with pytest, install `pytest-html`

```bash
pip install pytest-html
pytest --html=tests/reports/report.html
```

- Raw-change detection in `pipelines/raw_data_watcher.py` uses file SHA-256 hashed state in `.pipeline_state.json`.
---