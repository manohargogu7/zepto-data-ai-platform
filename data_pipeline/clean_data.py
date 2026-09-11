import pandas as pd


GBP_TO_INR = 105.50


def clean_books(books):
    """
    Clean scraped book records and convert them
    into the required data types.
    """

    df = pd.DataFrame(books)

    # Clean title and category text
    df["title"] = df["title"].astype(str).str.strip()
    df["category"] = df["category"].astype(str).str.strip()

    # Clean GBP price
    # Removes currency symbols and converts to numeric
    df["price_gbp"] = (
        df["price"]
        .astype(str)
        .str.replace("Â", "", regex=False)
        .str.replace("£", "", regex=False)
        .str.strip()
        .astype(float)
    )

    # Convert GBP to INR using the required fixed rate
    df["price_inr"] = df["price_gbp"] * GBP_TO_INR

    # Convert rating words to integers
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["star_rating"].map(rating_map)

    # Convert availability text to boolean
    df["in_stock"] = (
        df["availability"]
        .astype(str)
        .str.contains("In stock", case=False, na=False)
    )

    # Keep only the required final columns
    df = df[
        [
            "title",
            "category",
            "price_gbp",
            "price_inr",
            "rating",
            "in_stock"
        ]
    ]

    # Validate required fields
    if df["title"].isna().any() or (df["title"].str.len() == 0).any():
        raise ValueError("Some books have missing titles.")

    if df["price_gbp"].isna().any():
        raise ValueError("Some books have invalid GBP prices.")

    if df["price_inr"].isna().any():
        raise ValueError("Some books have invalid INR prices.")

    if not df["rating"].between(1, 5).all():
        raise ValueError("Rating must be an integer between 1 and 5.")

    return df


def save_cleaned_data(df):
    """Save the cleaned dataset as CSV."""
    output_path = "data_pipeline/data/books_cleaned.csv"

    df.to_csv(output_path, index=False)

    print(f"\nCleaned data saved to: {output_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    from scrape_pipeline import scrape_books

    print("Starting scraping...")

    raw_books = scrape_books()

    print("\nStarting cleaning...")

    cleaned_df = clean_books(raw_books)

    save_cleaned_data(cleaned_df)

    print("\nCleaning completed successfully!")

    print("\nData types:")
    print(cleaned_df.dtypes)

    print("\nFirst 5 cleaned rows:")
    print(cleaned_df.head())