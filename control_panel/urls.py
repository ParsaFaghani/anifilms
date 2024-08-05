from django.urls import path
from . import views

app_name = 'ControlPanel'

urlpatterns = [
    path('',views.anims,name='home'),
    path('accounts/',views.accounts,name='accounts'),
    path('create/',views.create_anim,name='create'),
    path('edit/<int:anim_id>',views.edit_anim,name='edit'),
    path('add_photo/<int:anim_id>',views.add_photo,name='add_photo'),
    path('change_ep/',views.change_ep, name='change_ep'),
    path('change_active_status/',views.change_active_status, name='change_active_status'),
    path('set_admin/',views.set_admin, name='set_admin'),
    path('<int:anim_id>',views.Upload, name='upload'),
    path('clear/<int:anim_id>', views.clear_database, name='clear_database'),
    path('delete', views.delete, name='delete'),
    path('msg/<str:redirct>/<str:message>',views.view_message,name='msg'),
]