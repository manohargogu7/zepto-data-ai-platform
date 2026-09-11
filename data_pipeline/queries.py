import sqlite3
import pandas as pd
from pathlib import Path


# Database path
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "zepto_books.db"


def run_query(query):
    """Execute a SQL query and return the results."""
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.execute(query)
    results = cursor.fetchall()

    connection.close()

    return results






if __name__ == "__main__":
    query = """
    SELECT title, price_gbp, price_inr
    FROM books
    LIMIT 5;
    """

    results = run_query(query)

    print("First 5 books:")
    for row in results:
        print(row)


    query_2 = """
    SELECT title, price_gbp, rating
    FROM books
    WHERE rating >= 4
    ORDER BY price_gbp DESC
    LIMIT 10;
    """

    results_2 = run_query(query_2)

    print("\nTop-rated books sorted by price:")
    for row in results_2:
        print(row) 




    query_3 = """
    SELECT DISTINCT category_name
    FROM categories
    ORDER BY category_name;
    """

    results_3 = run_query(query_3)

    print("\nDistinct book categories:")
    for row in results_3:
        print(row)

        query_4 = """
    SELECT title, price_gbp, category_id
    FROM books
    WHERE category_id IN (1, 2)
    ORDER BY price_gbp DESC
    LIMIT 10;
    """

    results_4 = run_query(query_4)

    print("\nBooks from selected categories:")
    for row in results_4:
        print(row)


    query_5 = """
SELECT title, price_gbp, price_inr
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp ASC;
"""

results_5 = run_query(query_5)

print("\nBooks priced between £20 and £40:")
for row in results_5:
    print(row)



    query_6 = """
    SELECT
        books.title,
        books.price_gbp,
        books.price_inr,
        books.rating,
        categories.category_name
    FROM books
    JOIN categories
        ON books.category_id = categories.category_id
    ORDER BY books.price_gbp DESC
    LIMIT 10;
    """

    results_6 = run_query(query_6)

    print("\nBooks with category information:")
    for row in results_6:
        print(row)




        connection = sqlite3.connect(DB_PATH)

    df_sql_1 = pd.read_sql(
        """
        SELECT title, price_gbp, price_inr, rating
        FROM books
        WHERE rating >= 4
        ORDER BY price_gbp DESC
        LIMIT 10;
        """,
        connection
    )

    print("\nPandas DataFrame from SQL Query 1:")
    print(df_sql_1)

    df_sql_2 = pd.read_sql(
        """
        SELECT
            books.title,
            books.price_gbp,
            categories.category_name
        FROM books
        JOIN categories
            ON books.category_id = categories.category_id
        ORDER BY books.price_gbp DESC
        LIMIT 10;
        """,
        connection
    )

    print("\nPandas DataFrame from SQL JOIN:")
    print(df_sql_2)

    connection.close()


        # Reproduce the SQL JOIN using pandas merge

    connection = sqlite3.connect(DB_PATH)

    books_df = pd.read_sql(
        """
        SELECT book_id, title, price_gbp, price_inr, rating, in_stock, category_id
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10;
        """,
        connection
    )

    categories_df = pd.read_sql(
        """
        SELECT category_id, category_name
        FROM categories;
        """,
        connection
    )

    connection.close()

    merged_df = pd.merge(
        books_df,
        categories_df,
        on="category_id",
        how="inner"
    )

    pandas_join_df = merged_df[
        ["title", "price_gbp", "price_inr", "rating", "category_name"]
    ]

    print("\nPandas JOIN using pd.merge():")
    print(pandas_join_df)

    print("\nSQL JOIN result:")
    print(df_sql_2)

    sql_compare = df_sql_2[
        ["title", "price_gbp", "category_name"]
    ].reset_index(drop=True)

    pandas_compare = pandas_join_df[
        ["title", "price_gbp", "category_name"]
    ].reset_index(drop=True)

    print("\nDo SQL JOIN and pandas merge match?")
    print(sql_compare.equals(pandas_compare))




    




         




