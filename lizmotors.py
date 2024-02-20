import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# This function will return the related urls using google search api
def search_google(query):
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.startswith("/url?") and not href.startswith("/url?q=https://www.google.com"):
            url = href.split("/url?q=")[1].split("&")[0]
            urls.append(urllib.parse.unquote(url))
    return urls


# This function will take the urls from above method and starts scraping the data
def scrape_website(url, query):
    response = requests.get(url)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    scraped_data = {'Query': query, 'URL': url, 'Content': response.text}
    
    return scraped_data

# This is our main function which will take the queries and give the expected output in csv format
def main():
    queries = [
        "Identify the industry in which Canoo operates, along with its size, growth rate, trends, and key players.",
        "Analyze Canoo's main competitors, including their market share, products or services offered, pricing strategies, and marketing efforts.",
        "Identify key trends in the market, including changes in consumer behavior, technological advancements, and shifts in the competitive landscape.",
        "Gather information on Canoo's financial performance, including its revenue, profit margins, return on investment, and expense structure."
    ]
    
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    csv_filename = f"scraped_data_{timestamp}.csv"

    all_keys = set()
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Query', 'URL', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for query in queries:
            print(f"Searching Google for '{query}'...")
            urls = search_google(query)
            print("Extracted URLs:", urls)
            urls = [url for url in urls if url.startswith("https://")]
            print("Filtered URLs:", urls)
            for url in urls:
                try:
                    data = scrape_website(url, query)
                    writer.writerow(data)
                    all_keys.update(data.keys())
                except Exception as e:
                    print(f"Error scraping {url} for query '{query}': {e}")
    
    print(f"Scraping complete. Output CSV file generated: {csv_filename}")

if __name__ == "__main__":
    main() 