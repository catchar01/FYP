import os
import django
import finnhub
import requests
from bs4 import BeautifulSoup
import random
from text_cleaning import clean_text

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'take2.settings')
django.setup()

from newsapp.models import NewsArticle
from django.utils import timezone
import datetime

# Define flexible content finder function, as it varies per page. Adjust if I have issues later.
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

US_stock_symbols = finnhub_client.stock_symbols('US')
stock_symbols = [stock['symbol'] for stock in US_stock_symbols]

# Select random stock symbol from list
random_stock_symbol = random.choice(stock_symbols)

news_items = finnhub_client.company_news(random_stock_symbol, _from="2023-06-01", to="2023-10-10") #maybe change date range later to a year from current day??

for item in news_items:
    stock_name = random_stock_symbol
    title = item.get('headline')
    unix_timestamp = item.get('datetime')
    url = item.get('url')

    if unix_timestamp and url:
        published_at = timezone.make_aware(datetime.datetime.fromtimestamp(unix_timestamp), timezone.get_default_timezone())
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_content = find_main_content(soup)
            if main_content:
                paragraphs = main_content.find_all('p')
                raw_content = ' '.join([paragraph.get_text().strip() for paragraph in paragraphs])
                cleaned_content = clean_text(raw_content)  # Use imported clean_text function
            else:
                cleaned_content = "Main content could not be found."
            
            news_article = NewsArticle(stock_name=random_stock_symbol, title=title, published_at=published_at, url=url, content=cleaned_content)
            news_article.save()
    else:
        print(f"Skipping article with missing data: {item}")

