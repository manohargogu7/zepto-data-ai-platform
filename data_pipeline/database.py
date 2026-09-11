import sqlite3
import pandas as pd
from pathlib import Path
# Project paths
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "books_cleaned.csv"
DB_PATH = BASE_DIR / "database" / "zepto_books.db"
def create_tables(connection):
    """Create the categories and books tables."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL NOT NULL,
            price_inr REAL NOT NULL,
            rating INTEGER NOT NULL,
            in_stock BOOLEAN NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    connection.commit()

    print("Database tables created successfully.")


if __name__ == "__main__":
     DB_PATH.parent.mkdir(parents=True, exist_ok=True)

     connection = sqlite3.connect(DB_PATH)

     create_tables(connection)

     connection.close()

     print("Database setup completed.")





def load_data():
    """Load cleaned CSV data into the SQLite database."""

    df = pd.read_csv(CSV_PATH)

    connection = sqlite3.connect(DB_PATH)
    connection.execute("DELETE FROM books")
    connection.execute("DELETE FROM categories")

    categories = sorted(df["category"].unique())

    for category in categories:
        connection.execute(
            "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
            (category,)
        )

    category_map = pd.read_sql(
        "SELECT category_id, category_name FROM categories",
        connection
    )

    df = df.merge(
        category_map,
        left_on="category",
        right_on="category_name",
        how="left"
    )

    for _, row in df.iterrows():
        connection.execute(
            """
            INSERT INTO books
            (title, price_gbp, price_inr, rating, in_stock, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                row["title"],
                row["price_gbp"],
                row["price_inr"],
                row["rating"],
                row["in_stock"],
                row["category_id"]
            )
        )

    connection.commit()
    connection.close()

    print(f"Loaded {len(df)} books into the database.")









     

    