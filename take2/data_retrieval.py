import os
import django
import finnhub
import requests
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'take2.settings')
django.setup()

from newsapp.models import NewsArticle
from django.utils import timezone
import datetime

# Define the flexible content finder function
def find_main_content(soup):
    for selector in [
        'article',
        ('div', {'class': 'article-body'}),
        ('div', {'class': 'post-content'}),
        'main',
        ('div', {'role': 'main'}),
    ]:
        if isinstance(selector, tuple):
            content = soup.find(*selector)
        else:
            content = soup.find(selector)
        if content:
            return content
    return None

finnhub_client = finnhub.Client(api_key="cmoku39r01qjn6781hjgcmoku39r01qjn6781hk0")

news_items = finnhub_client.company_news('AAPL', _from="2023-06-01", to="2023-10-10")

for item in news_items:
    stock_name = 'AAPL'
    unix_timestamp = item.get('datetime')
    url = item.get('url')

    if unix_timestamp and url:
        published_at = timezone.make_aware(datetime.datetime.fromtimestamp(unix_timestamp), timezone.get_default_timezone())
        
        # Initialize content to None
        content = None

        # Fetch and scrape the content of the URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_content = find_main_content(soup)
            if main_content:
                paragraphs = main_content.find_all('p')
                content = ' '.join([paragraph.get_text().strip() for paragraph in paragraphs])
                print(content)
            else:
                content = "Main content could not be found."

        news_article = NewsArticle(stock_name=stock_name, published_at=published_at, url=url, content=content)
        news_article.save()
    else:
        print(f"Skipping article with missing data: {item}")

