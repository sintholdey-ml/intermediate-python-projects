import argparse
import csv
import json
import re
import sys
import requests
from bs4 import BeautifulSoup

def scrape_quotes(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f" Error fetching URL: {e}")
        sys.exit(1)


    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    quotes = soup.find_all("div", class_="quote")

    if quotes:
        for q in quotes:
            text = q.find("span", class_="text").get_text(strip=True)
            author = q.find("small", class_="author").get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]
            results.append({
                "quote": text,
                "author": author,
                "tags": ", ".join(tags)
            })

    else:
        headings = soup.find_all(["h1", "h2", "h3"])
        for h in headings:
            text = h.get_text(strip= True)
            if text:
                results.append({"title": text, "tag": h.name})

    return results

def save_to_csv(data, filename):
    if not data:
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f" Data saved successfully to CSV: {filename}")


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data,f , indent =4, ensure_ascii=False)
    print(f" Data saved successfully to JSON: {filename}")


def main():
    parser = argparse.ArgumentParser(description="Python CLI Web Scraper & Data Extractor")
    parser.add_argument("-u", "--url", default="https://quotes.toscrape.com", help="Target URL to scrape (default: https://quotes.toscrape.com)")
    parser.add_argument("-o", "--output", default="scraped_data.json", help="Output file path (.csv or .json)")

    args = parser.parse_args()

    print(f" Fetching data from: {args.url}")
    scraped_data = scrape_quotes(args.url)

    if not scraped_data:
        print(" No data extracted.")
        return

    print(f" Extracted {len(scraped_data)} items successfully.\n")

    output_file = args.output
    if output_file.endswith(".csv"):
        save_to_csv(scraped_data, output_file)
    else:
        save_to_json(scraped_data, output_file)

if __name__ == "__main__":
    main()

