from django.db import models

# Create your models here.
class Article(models.Model):
    text = models.TextField()
    url = models.URLField(blank=True)
    score = models.IntegerField()
    verdict = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}... ({self.verdict})"
