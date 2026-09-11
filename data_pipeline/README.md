# Data Pipeline

## Overview

This module implements an end-to-end book data pipeline using
Books to Scrape.

The pipeline performs:

1. Web scraping
2. Data cleaning
3. GBP to INR conversion
4. SQLite database creation
5. SQL querying
6. Pandas analysis and SQL JOIN validation

## Data Source

Source: Books to Scrape

The pipeline collects book information programmatically without
manual copy/paste.

The dataset contains 144 books across 4 categories.

## Currency Conversion

A fixed conversion rate is used:

**1 GBP = 105.50 INR**

The INR price is calculated as:

`price_inr = price_gbp × 105.50`

## Data Cleaning

The cleaning stage:

- Removes unwanted whitespace from titles and categories
- Converts prices to numeric values
- Converts ratings to integer values from 1 to 5
- Converts stock status to Boolean values
- Removes invalid/incomplete records
- Calculates `price_inr` using the fixed exchange rate
- Saves the cleaned dataset as CSV

## Database Design

SQLite is used as the relational database.

### categories

| Column | Type | Constraint |
|---|---|---|
| category_id | INTEGER | Primary Key |
| category_name | TEXT | UNIQUE, NOT NULL |

### books

| Column | Type | Constraint |
|---|---|---|
| book_id | INTEGER | Primary Key |
| title | TEXT | NOT NULL |
| price_gbp | REAL | NOT NULL |
| price_inr | REAL | NOT NULL |
| rating | INTEGER | NOT NULL |
| in_stock | INTEGER | NOT NULL |
| category_id | INTEGER | Foreign Key |

The `books.category_id` column references
`categories.category_id`.

## Files

- `scrape_pipeline.py` - Scrapes book data
- `clean_data.py` - Cleans and transforms the data
- `database.py` - Creates and loads the SQLite database
- `queries.py` - Runs SQL queries and compares SQL JOIN with Pandas merge
- `run_pipeline.py` - Runs the complete pipeline

## Running the Pipeline

From the project root:

```powershell
python data_pipeline\run_pipeline.py





```markdown
## SQL Query Coverage

The `queries.py` module demonstrates multiple SQL operations:

1. `SELECT` - retrieves book information
2. `WHERE` - filters books based on rating and price
3. `ORDER BY` - sorts books by price
4. `LIMIT` - restricts the number of returned rows
5. `DISTINCT` - identifies unique book categories
6. `IN` - filters books belonging to selected categories
7. `BETWEEN` - filters books within a price range
8. `JOIN` - combines the `books` and `categories` tables using the foreign key relationship

The SQL query outputs are saved in:

`data_pipeline/outputs/sql_results.txt`

## Pandas SQL Analysis

At least two SQL query results are loaded into Pandas DataFrames using `pd.read_sql()`.

This allows the SQL results to be analyzed and compared using Pandas.

The SQL JOIN result is also loaded into a Pandas DataFrame.

## SQL JOIN and Pandas Merge Validation

The relational JOIN between `books` and `categories` is reproduced in memory using `pandas.merge()`.

The following relationship is used:

`books.category_id = categories.category_id`

The SQL JOIN result and Pandas merge result are compared using matching columns and row ordering.

The validation produced:

```text
Do SQL JOIN and pandas merge match?
True



## Validation Results

The completed pipeline was tested end-to-end successfully.

- 144 books were scraped and cleaned.
- 4 book categories were collected.
- SQLite database contains 144 book records.
- The database contains 4 category records.
- Ratings are stored as integers from 1 to 5.
- Stock status is stored as a Boolean-compatible value.
- GBP prices are converted to INR using the fixed rate of 1 GBP = 105.50 INR.
- SQL queries were executed successfully.
- SQL JOIN results were reproduced using `pandas.merge()`.
- SQL JOIN and Pandas merge results were validated and matched successfully.