from django.contrib import admin
from django.urls import path , re_path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from user.forms import LoginForm
from django.contrib.auth import views as auth_views
from anim import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('ControlPanel/', include('control_panel.urls')),
    path('accounts/',include('user.urls')),
    path('',include('anim.urls')),
    path('api/', include('api.urls'), name='api'),
    path('comment/', include('comment.urls')),
    path('rating/', include('rating.urls')),
    path('rosetta/', include('rosetta.urls')),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
