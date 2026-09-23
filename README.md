# Zepto Data & AI Platform

A complete end-to-end data and AI project covering data engineering, analytics, machine learning, and a RAG-based support assistant.

## Project Overview

This project is organized into three main modules:

1. **Data Pipeline** — Web scraping, data cleaning, SQLite database creation, and SQL/Pandas analysis.
2. **Analytics & Machine Learning** — Exploratory data analysis, classification, imbalance handling, Random Forest tuning, regression, and a saved ML pipeline.
3. **Support Assistant** — A RAG-based Zepto policy support assistant using local policy documents, a vector database, retrieval, LangGraph workflow orchestration, and a FastAPI interface.

## Project Structure

```text
zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── data/
│   ├── database/
│   ├── outputs/
│   ├── scrape_pipeline.py
│   ├── clean_data.py
│   ├── database.py
│   ├── queries.py
│   ├── run_pipeline.py
│   └── README.md
│
├── analytics/
│   ├── outputs/
│   │   └── best_titanic_pipeline.joblib
│   ├── support_assistant/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   └── README.md
│
├── support_assistant/
│   ├── docs/
│   ├── chroma_db/
│   ├── assistant.py
│   ├── ingest.py
│   ├── retrieve.py
│   ├── main.py
│   └── README.md
│
└── README.md
Module 1 — Data Pipeline

The data pipeline module collects book data from the web, cleans and validates the dataset, stores it in SQLite, and performs SQL and Pandas analysis.

Main components
Web scraping using requests and BeautifulSoup
Data cleaning and validation using Pandas
SQLite database creation
SQL queries using SQLite
Pandas read_sql
SQL-to-Pandas result comparison
Reproducible pipeline execution
Module 2 — Analytics & Machine Learning

The analytics module contains a complete Titanic dataset analysis and machine learning workflow.

Exploratory Data Analysis
Dataset profiling
Missing-value analysis and handling
Univariate analysis
IQR-based outlier analysis
Bivariate survival analysis
Correlation analysis
Multivariate analysis
Standardization demonstration
Machine Learning

Classification models:

Logistic Regression
Decision Tree
Random Forest

Additional experiments:

Baseline classification
Class-weight balancing
SMOTE
Random Forest GridSearchCV
Out-of-bag evaluation

Regression:

Linear Regression
MAE
RMSE
R²
Adjusted R²
Residual analysis
Heteroscedasticity assessment

A complete fitted Titanic classification pipeline is saved as:

analytics/outputs/best_titanic_pipeline.joblib

Module 3 — Support Assistant

The support assistant is a retrieval-augmented generation system designed to answer questions about Zepto policies.

Main components
Local policy documents
Document ingestion
Text embeddings
Chroma vector database
Semantic retrieval
Intent classification
LangGraph workflow
Answer generation
Source attribution
Confidence score
FastAPI REST API
Swagger documentation

The assistant exposes a POST /ask endpoint for policy questions.

Swagger documentation is available when the API is running at:

http://127.0.0.1:8000/docs

Technology Stack
Python
Pandas
NumPy
Matplotlib
Seaborn
Scikit-learn
Imbalanced-learn
Joblib
SQLite
Requests
BeautifulSoup
Sentence Transformers
ChromaDB
LangGraph
FastAPI
Uvicorn
Jupyter Notebook
Reproducibility

All modules are designed to run locally using the project's Python environment.

No paid external services are required.

Generated databases, cached files, Python cache files, and local environment files are excluded from version control where appropriate.

Author

Gogu Manohar

B.Tech Biotechnology
National Institute of Technology, Calicut