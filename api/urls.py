from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('anime/', views.AnimeListView.as_view(), name='anime-list'),
]