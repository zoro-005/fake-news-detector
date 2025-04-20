from django.urls import path 
from . import views 

app_name = 'detector'

urlpatterns=[
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
]