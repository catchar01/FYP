from django.shortcuts import render
from .models import NewsArticle

def index(request):
    articles = NewsArticle.objects.all()
    return render(request, 'newsapp/index.html', {'articles': articles})