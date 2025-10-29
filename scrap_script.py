import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

BASE_URL = "https://sanskrit.uohyd.ac.in/Corpus/"

def fetch_page(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in " _-()" else "_" for c in name).strip()

def parse_main_page(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for row in soup.find_all('tr'):
        links = []
        for a in row.find_all('a'):
            href = a.get('href')
            text = a.get_text(strip=True)
            if href:
                links.append((text, urljoin(BASE_URL, href)))
        if links:
            raw_text = row.get_text(separator=" ", strip=True)
            for text, _ in links:
                raw_text = raw_text.replace(text, "")
            book_name = raw_text.split(":")[0].strip() or "unknown"
            books.append({"book_name": book_name, "links": links})
    return books

def clean_sanskrit_text(text):
    """Fix encoding and remove metadata."""
    # 1️⃣ Fix UTF-8 decoding issue
    # If garbled, re-encode/decode to UTF-8
    try:
        # Try correcting wrongly-decoded UTF-8
        text = text.encode('latin1').decode('utf-8')
    except Exception:
        pass

    # 2️⃣ Remove BOM or stray chars
    text = text.replace('\ufeff', '').strip()

    # 3️⃣ Remove metadata: skip header until first empty line or Sanskrit line
    lines = text.splitlines()
    cleaned = []
    started = False
    for line in lines:
        if not started:
            # if line has Sanskrit (Devanagari Unicode range \u0900-\u097F)
            if re.search(r'[\u0900-\u097F]', line):
                started = True
                cleaned.append(line.strip())
        else:
            cleaned.append(line.strip())
    return "\n".join(cleaned).strip()

def download_and_save(book, output_dir="dataset"):
    folder = sanitize_filename(book["book_name"])
    dir_path = os.path.join(output_dir, folder)
    os.makedirs(dir_path, exist_ok=True)

    for label, link in book["links"]:
        try:
            r = requests.get(link)
            r.raise_for_status()
            content = r.content  # get raw bytes
        except Exception as e:
            print(f"Failed to download {link}: {e}")
            continue

        # Decode properly
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            text = content.decode('latin1')

        # Convert HTML → text if necessary
        if "<html" in text.lower():
            soup = BeautifulSoup(text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)

        text = clean_sanskrit_text(text)

        filename = sanitize_filename(label) + ".txt"
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved {filepath}")

def main():
    html = fetch_page(BASE_URL)
    books = parse_main_page(html)
    print(f"Found {len(books)} books.")
    for book in books:
        download_and_save(book)

if __name__ == "__main__":
    main()
