from . import views
from . import api
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.update_ticket, name='update_ticket'),
    path('login/', auth_views.LoginView.as_view(success_url='approve_updates'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('success/', views.success, name='success'),
    path('list/', views.update_KA_json, name='update_KA_json'),
    path('approve_updates/', views.approve_updates, name='approve_updates')
]