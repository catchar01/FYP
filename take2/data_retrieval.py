import os
import django
import finnhub

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'take2.settings')
django.setup()

from newsapp.models import NewsArticle
from django.utils import timezone #instead of parsedatetime because that expects ISO-format but FH gives date in UNIX.
import datetime

finnhub_client = finnhub.Client(api_key="cmoku39r01qjn6781hjgcmoku39r01qjn6781hk0")

news_items = finnhub_client.company_news('AAPL', _from="2023-06-01", to="2023-10-10")

news_items = finnhub_client.company_news('AAPL', _from="2023-06-01", to="2023-10-10")

for item in news_items:
    stock_name = 'AAPL'
    unix_timestamp = item.get('datetime')
    url = item.get('url')

    if unix_timestamp and url:
        published_at = timezone.make_aware(datetime.datetime.fromtimestamp(unix_timestamp), timezone.get_default_timezone())
        news_article = NewsArticle(stock_name=stock_name, published_at=published_at, url=url)
        news_article.save()
    else:
        print(f"Skipping article with missing data: {item}")