from django.urls import path, re_path, include
from . import views
from user import views as user_views

app_name = 'anime'


urlpatterns = [
    path('home',views.home,name='home'),
    path('',views.list, name='list'),
    path('video/<int:video_id>',views.view_video, name='video'),
    path('<str:anim_name>',views.view, name='view'),
    path('tag/<str:slug>/', views.tagged, name="tagged"),
    path('save/<int:pk>',views.SaveView, name='anim_save'),
    re_path(r'^download/(?P<media_key>.+)/$', views.get_media, name='get_media'),
]
