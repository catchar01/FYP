import os
from wordcloud import WordCloud
from django.conf import settings
from django.shortcuts import render
from .models import NewsArticle, FavouriteStock
from django.http import JsonResponse
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

def generate_wordcloud():
    # Aggregate text data
    all_content = " ".join(article.content for article in NewsArticle.objects.all() if article.content)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_content)

    # Ensure static directory exists
    static_dir = os.path.join(settings.BASE_DIR, 'newsapp', 'static')
    os.makedirs(static_dir, exist_ok=True)

    # Path to save word cloud image within the app's static directory
    wordcloud_image_path = os.path.join(static_dir, 'wordcloud.png')

    wordcloud.to_file(wordcloud_image_path)

def index(request):
    wordcloud_image_url = generate_wordcloud()
    context = {'wordcloud_image_url': wordcloud_image_url}
    return render(request, 'index.html', context)

def stocks(request):
    stock_names = NewsArticle.objects.values_list('stock_name', flat=True).distinct()

    if request.user.is_authenticated:
        # Only query favourite stocks if user = authenticated
        favourite_stocks = FavouriteStock.objects.filter(user=request.user).values_list('stock_name', flat=True)
    else:
        # If the user != authenticated, set favourite_stocks to empty list
        favourite_stocks = []
    
    return render(request, 'stocks.html', {'stock_names': stock_names, 'favourite_stocks': favourite_stocks})

def stock_articles(request):
    stock_name = request.GET.get('stock_name')
    articles = list(NewsArticle.objects.filter(stock_name=stock_name).values('title','url','published_at')[:2])
    return JsonResponse(articles, safe=False)

###log in stuff
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@require_POST
@csrf_exempt  # Only for testing purposes. Remove this and handle CSRF properly in production
def toggle_favourite(request):
    try:
        data = json.loads(request.body)
        stock_name = data['stock_name']
    except (KeyError, json.JSONDecodeError) as e:
        return HttpResponseBadRequest('Invalid data')

    user = request.user

    favourite, created = FavouriteStock.objects.get_or_create(user=user, stock_name=stock_name)
    if not created:
        # If favourite already exists, delete
        favourite.delete()
        is_favourite = False
    else:
        # If favourite just created, it's now a favourite
        is_favourite = True

    # Return JSON response indicating success and whether stock is a favourite
    return JsonResponse({'success': True, 'is_favourite': is_favourite})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def is_favourite(request):
    stock_name = request.GET.get('stock_name')
    is_favourite = FavouriteStock.objects.filter(user=request.user, stock_name=stock_name).exists()
    return JsonResponse({'is_favourite': is_favourite})