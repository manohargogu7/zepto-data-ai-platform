from scrape_pipeline import scrape_books
from clean_data import clean_books, save_cleaned_data
from database import create_tables, load_data, DB_PATH
import sqlite3


def main():
    print("=" * 60)
    print("ZEPTO DATA PIPELINE")
    print("=" * 60)

    print("\n[1/4] Scraping books...")
    books = scrape_books()
    print(f"Scraped {len(books)} books.")

    print("\n[2/4] Cleaning data...")
    cleaned_df = clean_books(books)
    save_cleaned_data(cleaned_df)
    print(f"Cleaned {len(cleaned_df)} books.")

    print("\n[3/4] Creating database tables...")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    create_tables(connection)
    connection.close()

    print("\n[4/4] Loading cleaned data...")
    load_data()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()