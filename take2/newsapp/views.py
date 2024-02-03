import os
from wordcloud import WordCloud
from django.conf import settings
from django.shortcuts import render
from .models import NewsArticle
from django.http import JsonResponse

def generate_wordcloud():
    # Aggregate text data
    all_content = " ".join(article.content for article in NewsArticle.objects.all() if article.content)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_content)

    # Ensure the static directory exists
    static_dir = os.path.join(settings.BASE_DIR, 'newsapp', 'static')
    os.makedirs(static_dir, exist_ok=True)

    # Path to save word cloud image within the app's static directory
    wordcloud_image_path = os.path.join(static_dir, 'wordcloud.png')

    # Save word cloud image
    wordcloud.to_file(wordcloud_image_path)

def index(request):
    wordcloud_image_url = generate_wordcloud()
    context = {'wordcloud_image_url': wordcloud_image_url}
    return render(request, 'index.html', context)

def stocks(request):
    stock_names = NewsArticle.objects.values_list('stock_name', flat=True).distinct()
    return render(request, 'stocks.html', {'stock_names': stock_names})

def stock_articles(request):
    stock_name = request.GET.get('stock_name')
    articles = list(NewsArticle.objects.filter(stock_name=stock_name).values('title','url','published_at')[:2])
    return JsonResponse(articles, safe=False)