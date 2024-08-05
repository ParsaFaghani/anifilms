from django.urls import path, re_path
from . import views as user_views
from user.forms import LoginForm
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('signup/', user_views.signupView, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit/', user_views.editView, name='edit_profile'),
    path('change_password/', user_views.change_password, name='change_password'),
    path('follow/', user_views.followView.as_view(), name='follow'),
    path('<str:username>/', user_views.profileView, name='profile'),
    path('activate/<slug:uidb64>/<slug:token>/', user_views.activate, name='activate'),
]
