import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"


def get_soup(url):
    """Download a webpage and return its BeautifulSoup object."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def test_connection():
    """Test whether Books to Scrape is reachable."""
    soup = get_soup(BASE_URL)

    title = soup.title.get_text(strip=True)

    print("Connection successful!")
    print(f"Website title: {title}")


def get_categories():
    """Get book categories and their URLs."""
    soup = get_soup(BASE_URL)

    categories = []

    category_links = soup.select("ul.nav-list ul li a")

    for link in category_links:
        category_name = link.get_text(strip=True)
        category_url = link.get("href")

        if category_url:
            full_url = urljoin(BASE_URL, category_url)

            categories.append(
                {
                    "category": category_name,
                    "url": full_url
                }
            )

    return categories


def scrape_category(category_name, category_url):
    """Scrape all books from one category."""
    books = []

    current_url = category_url

    while current_url:
        print(f"Scraping category: {category_name}")
        print(f"URL: {current_url}")

        soup = get_soup(current_url)

        book_cards = soup.select("article.product_pod")

        for book in book_cards:

            title_tag = book.select_one("h3 a")
            price_tag = book.select_one(".price_color")
            rating_tag = book.select_one(".star-rating")
            availability_tag = book.select_one(".availability")

            title = ""

            if title_tag:
                title = title_tag.get("title", "").strip()

            price = ""

            if price_tag:
                price = price_tag.get_text(strip=True)

            star_rating = ""

            if rating_tag:
                classes = rating_tag.get("class", [])

                if len(classes) > 1:
                    star_rating = classes[-1]

            availability = ""

            if availability_tag:
                availability = availability_tag.get_text(
                    " ",
                    strip=True
                )

            books.append(
                {
                    "title": title,
                    "price": price,
                    "star_rating": star_rating,
                    "availability": availability,
                    "category": category_name
                }
            )

        next_link = soup.select_one("li.next a")

        if next_link:
            next_url = next_link.get("href")

            if next_url:
                current_url = urljoin(
                    current_url,
                    next_url
                )
            else:
                current_url = None

        else:
            current_url = None

    return books


def scrape_books():
    """Scrape books from at least three categories."""
    categories = get_categories()

    print(f"\nTotal categories found: {len(categories)}")

    # Use the first four categories.
    # This gives us a safe margin above the required 60 books.
    selected_categories = categories[:4]

    print("\nSelected categories:")

    for category in selected_categories:
        print(f"- {category['category']}")

    all_books = []

    for category in selected_categories:

        category_books = scrape_category(
            category["category"],
            category["url"]
        )

        all_books.extend(category_books)

    print(f"\nTotal books scraped: {len(all_books)}")

    if len(all_books) < 60:
        raise ValueError(
            f"Only {len(all_books)} books were scraped. "
            "The assignment requires at least 60 books."
        )

    return all_books


if __name__ == "__main__":

    test_connection()

    books = scrape_books()

    print("\nFirst 5 scraped books:")

    for book in books[:5]:
        print(book)