import csv
import json
import requests
import sqlite3

from bs4 import BeautifulSoup

URL = "http://books.toscrape.com/"

def create_table():
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                currency TEXT,
                price REAL
                
            );
        """
    )
    con.close()
    print("DAtabase and table created successfully.")


def insert_book(title, currency, price):
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
         "INSERT INTO books (title, currency, price) VALUES (?, ?, ?)",
         (title, currency, price),
    )
    con.commit()
    con.close()


def scrape_book (url):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    # Set encoding explicityly to heandle special characters correctly
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    book_elements = soup.find_all("article", class_="product_pod")

    books =[]
    for book in book_elements:
        title = book.h3.a['title']
        price_text = book.find("p", class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])
        # insert_book(title, currency, price)
        books.append(
            {
                "title": title,
                "currency": currency,
                "price": price,
            }
        )
    
    print("All books are scrapped ")
    return books

def save_to_json(books):

    with open("books.json", "w", encoding = "utf-8") as f:
        json.dump(books, f, indent = 4, ensure_ascii = False)

def save_to_csv(books):

    with open("books.csv", "w", newline= "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "currency", "price"])
        writer.writeheader()
        writer.writerows(books)


create_table()
books = scrape_book(URL)
save_to_json(books)
save_to_csv(books)

# git init => initialize git repository
# git status => if you want to check what are the status of files
# git diff => if you want to check what are the changes
# git add. => track all file in current directory
# git commit -m "your message"
# copy paste git code from github

###########################
# change the code
# git add .
# git commit -m "Your message"
# git push
############################
