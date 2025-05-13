import requests
from bs4 import BeautifulSoup
import feedparser
import json

# Function to fetch and parse the RSS feed
def fetch_rss_articles(rss_url):
    rss_url = "https://www.thehindu.com/news/national/feeder/default.rss"
    feed = feedparser.parse(rss_url)
    articles = []
    
    # Iterate through the feed entries and extract article details
    for entry in feed.entries[:50]:  # Limit to 50 articles
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.description,
        })
    return articles

def scrapeData():
    # RSS URL you provided
    rss_url = "https://www.thehindu.com/news/national/feeder/default.rss"
    
    # Fetch the articles
    articles = fetch_rss_articles(rss_url)
    
    # Save the articles to a JSON file
    file_path = 'fetched_articles.json'
    with open(file_path, 'w') as json_file:
        json.dump(articles, json_file, indent=4)
    
    print(f"Fetched articles saved to {file_path}")