# SmartCredit Cloud - ELT Pipeline & MLOps Architecture

End-to-end modern data stack and MLOps pipeline for automated credit risk scoring. This project implements a robust **ELT (Extract, Load, Transform)** workflow, moving from automated data ingestion and modern data warehousing to analytics engineering, data quality governance, machine learning inference, containerization, and cloud deployment readiness.

## Core Data Engineering & MLOps Stack

- **Modern ELT Pipeline (`dlt` & `dbt`):** 
  - **Extract & Load (`dlt`):** Automated ingestion of raw financial and credit datasets into the data store.
  - **Transform (`dbt`):** Analytics engineering layer performing data cleansing, staging models, dimensional mart modeling, and feature engineering.
- **Data Warehousing (`DuckDB`):** High-performance analytical columnar database serving as the local data warehouse and feature store.
- **Data Quality & Governance (`dbt tests`):** Automated assertions ensuring referential integrity, uniqueness, and non-null constraints across data pipelines.
- **Machine Learning (`XGBoost` & `Scikit-Learn`):** Predictive model trained on features engineered by the dbt pipeline.
- **Model Serving & API (`FastAPI`):** Low-latency inference web service built for production serving.
- **Containerization & CI/CD (`Docker` & `GitHub Actions`):** Isolated container builds and automated testing workflows.
- **Cloud Infrastructure (`AWS`):** Target deployment architecture for scalable production environments.

## Project Structure

```text
smartcredit-cloud-mlops/
├── .github/workflows/    # CI/CD automation pipelines
├── dbt_smartcredit/      # ELT transformation models, staging/marts, and data quality tests
├── data/                 # DuckDB database and source datasets
├── models/               # Serialized machine learning artifacts (.pkl)
├── app.py                # FastAPI inference service
├── Dockerfile            # Container configuration
└── requirements.txt      # Production Python dependencies
