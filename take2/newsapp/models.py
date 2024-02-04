from django.db import models

class NewsArticle(models.Model):
    stock_name = models.CharField(max_length=100)
    title = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()
    url = models.URLField()
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock_name} ({self.published_at.strftime('%Y-%m-%d %H:%M:%S')})"

from django.contrib.auth.models import User

class FavouriteStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'stock_name',)