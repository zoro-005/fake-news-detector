from django.contrib import admin
from .models import Article
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['text', 'score', 'verdict', 'timestamp']
    list_filter = ['verdict', 'timestamp']
    search_fields = ['text']
