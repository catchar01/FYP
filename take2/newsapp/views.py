import os
from wordcloud import WordCloud
from django.conf import settings
from django.shortcuts import render
from .models import NewsArticle

def generate_wordcloud():
    # Aggregate text data
    all_content = " ".join(article.content for article in NewsArticle.objects.all() if article.content)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_content)

    # Ensure the static/newsapp directory exists
    static_dir = os.path.join(settings.BASE_DIR, 'newsapp', 'static', 'newsapp')
    os.makedirs(static_dir, exist_ok=True)

    # Path to save word cloud image within the app's static directory
    wordcloud_image_path = os.path.join(static_dir, 'wordcloud.png')

    # Save word cloud image
    wordcloud.to_file(wordcloud_image_path)

def index(request):
    wordcloud_image_url = generate_wordcloud()
    context = {'wordcloud_image_url': wordcloud_image_url}
    return render(request, 'newsapp/index.html', context)
