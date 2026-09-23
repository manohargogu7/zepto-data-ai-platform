# Zepto Data & AI Platform

A complete data and AI platform project containing three independent modules:

1. Data Pipeline
2. Analytics & Machine Learning
3. AI Support Assistant

The project is organized as one public GitHub repository with all three modules at the root level.

---

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
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   ├── outputs/
│   │   └── best_titanic_pipeline.joblib
│   └── README.md
│
├── support_assistant/
│   ├── docs/
│   │   ├── doc_01.txt
│   │   ├── doc_02.txt
│   │   ├── doc_03.txt
│   │   ├── doc_04.txt
│   │   ├── doc_05.txt
│   │   ├── doc_06.txt
│   │   ├── doc_07.txt
│   │   └── doc_08.txt
│   ├── assistant.py
│   ├── ingest.py
│   ├── retrieve.py
│   ├── main.py
│   ├── Dockerfile
│   └── README.md
│
├── requirements.txt
├── .gitignore
└── README.md
1. Setup
Requirements
Python 3.11+
Git
VS Code or another Python-compatible IDE

All Python dependencies are listed in the root:

requirements.txt
Create and activate virtual environment

From the project root:

Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Install dependencies
pip install -r requirements.txt
2. Data Pipeline
Purpose

The data pipeline collects book data, cleans and transforms the dataset, stores the cleaned data in SQLite, and executes SQL analysis queries.

Main components
scrape_pipeline.py — collects the source book data.
clean_data.py — cleans and transforms the collected data.
database.py — creates and populates the SQLite database.
queries.py — executes analytical SQL queries.
run_pipeline.py — runs the pipeline end to end.
Run

From the project root:

python data_pipeline\run_pipeline.py

The pipeline produces:

data_pipeline/data/books_cleaned.csv
data_pipeline/database/zepto_books.db
data_pipeline/outputs/sql_results.txt
Design Decisions
Python/Pandas are used for data collection and cleaning because they provide simple and reproducible tabular data processing.
SQLite is used as the database because the assignment does not require an external database server.
SQL queries are used for aggregation and analysis to demonstrate relational data processing.
A reproducible pipeline script is provided so the complete workflow can be executed from a single command.
3. Analytics & Machine Learning
Purpose

The analytics module performs exploratory data analysis and builds machine-learning models using the Titanic dataset.

Notebook order

The notebooks should be executed in this order:

01_eda.ipynb
02_modeling.ipynb
01 — Exploratory Data Analysis

The EDA notebook covers:

Dataset loading
Dataset dimensions
Missing-value analysis
Data cleaning
IQR-based outlier detection
Univariate analysis
Bivariate survival analysis
Correlation analysis
Multivariate analysis
Standardization demonstration
Written interpretations
02 — Modeling

The modeling notebook covers:

Train/test split
Stratified splitting
Preprocessing pipeline
Missing-value imputation
Feature scaling
One-hot encoding
Logistic Regression
Decision Tree
Random Forest
Classification metrics
Confusion matrices
ROC-AUC
Class imbalance
Class weighting
SMOTE
Random Forest GridSearchCV
OOB evaluation
Fare regression
Residual analysis
Model comparison
Final pipeline saving and reloading
Run

Start Jupyter from the project root:

jupyter notebook

Then open:

analytics/01_eda.ipynb

Run it first.

Then open:

analytics/02_modeling.ipynb

and run it second.

The final trained pipeline is saved as:

analytics/outputs/best_titanic_pipeline.joblib
Design Decisions
Pandas is used for data manipulation and analysis.
Seaborn/Matplotlib are used for visualization.
A ColumnTransformer keeps numerical and categorical preprocessing separate.
Pipeline is used to prevent preprocessing leakage between training and testing data.
Stratified splitting preserves the target-class distribution.
Logistic Regression, Decision Tree, and Random Forest provide multiple classification approaches for comparison.
SMOTE and class weighting are evaluated to address class imbalance.
GridSearchCV is used to tune the Random Forest.
The final preprocessing and model are saved together using joblib so the complete pipeline can be reused on new data.
4. AI Support Assistant
Purpose

The support assistant answers Zepto policy questions using a local document knowledge base, ChromaDB retrieval, LangGraph orchestration, and a FastAPI API.

The module contains eight policy documents.

Architecture
Policy Documents
      |
      v
Document Ingestion
      |
      v
Embeddings
      |
      v
ChromaDB
      |
      v
User Question
      |
      v
Intent Classification
      |
      +----------------------+
      |                      |
      v                      v
Policy Question          Other Question
      |                      |
      v                      v
Top-3 Retrieval          Direct Answer
      |
      v
Answer Generation
      |
      v
FastAPI JSON Response
Main components
docs/ — eight source policy documents.
ingest.py — loads and embeds the documents into ChromaDB.
retrieve.py — performs top-3 similarity retrieval.
assistant.py — defines the LangGraph workflow, intent classification, prompt, retrieval and answer generation.
main.py — exposes the assistant through FastAPI.
Dockerfile — provides a containerized local runtime.
Build the knowledge base

From the project root:

python support_assistant\ingest.py

This creates the local ChromaDB knowledge base.

Run the API

From the project root:

uvicorn support_assistant.main:api --reload --port 8000

The API endpoint is:

POST /ask
Example request
{
  "question": "What is the return policy?"
}
Example response
{
  "answer": "Based on the retrieved context: ...",
  "sources": ["doc_01.txt"],
  "confidence": 0.9
}

A non-policy question is handled directly:

{
  "question": "What is the capital of India?"
}

Example response:

{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
Mock LLM Mode

The assistant supports a mock mode using:

MOCK_LLM=1

Mock mode is the default when the variable is unset.

In mock mode:

Intent classification uses a keyword heuristic.
No external LLM call is made.
Retrieved policy questions return an answer beginning with:
Based on the retrieved context:
Non-policy questions return the fixed direct-answer response.
LangGraph Workflow

The graph contains these named nodes:

classify_intent
retrieve_and_answer
direct_answer

Conditional routing sends policy questions to retrieval and other questions to the direct-answer node.

The assistant uses:

TypedDict state
StateGraph
Conditional edges
ChromaDB
Sentence Transformers
Top-3 retrieval
Structured prompting
Retry logic for optional real LLM calls
Pydantic response validation
Design Decisions
ChromaDB provides a local vector database without requiring a paid external service.
Sentence Transformers creates embeddings locally.
Top-3 retrieval provides focused context for answering policy questions.
LangGraph makes the assistant workflow explicit and modular.
MOCK_LLM makes the application reproducible without requiring an API key.
FastAPI provides a simple REST interface.
Pydantic validates the API response structure.
The optional real-LLM path includes retry logic to handle temporary failures.
5. Docker

The Support Assistant includes a Dockerfile.

From the support_assistant directory:

cd support_assistant
docker build -t zepto-support-assistant .

Run the container:

docker run -p 7860:7860 zepto-support-assistant

The FastAPI service runs on:

http://localhost:7860
6. Reproducibility

The project is designed so that the major workflows can be reproduced locally.

Data Pipeline
python data_pipeline\run_pipeline.py
Analytics
jupyter notebook

Run:

analytics/01_eda.ipynb
analytics/02_modeling.ipynb

in that order.

Support Assistant
python support_assistant\ingest.py
uvicorn support_assistant.main:api --reload --port 8000
7. Technology Stack
Module	Technologies
Data Pipeline	Python, Pandas, Requests, BeautifulSoup, SQLite, SQL
Analytics	Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, imbalanced-learn, Joblib
Support Assistant	Python, LangGraph, ChromaDB, Sentence Transformers, FastAPI, Pydantic
Deployment	Docker
8. Git Workflow

The project uses Git for version control.

Development included a feature branch and a merge back into the main branch.

The repository contains multiple commits showing the development history.

9. Submission

The complete project is contained in one public GitHub repository.

The repository contains:

data_pipeline/
analytics/
support_assistant/
requirements.txt
README.md

All three modules can be run locally without paid services.