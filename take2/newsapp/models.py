from django.db import models

class NewsArticle(models.Model):
    stock_name = models.CharField(max_length=100)
    title = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField()
    url = models.URLField()
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock_name} ({self.published_at.strftime('%Y-%m-%d %H:%M:%S')})"
