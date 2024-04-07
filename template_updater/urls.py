from . import views
from . import api
from django.urls import path, include

urlpatterns = [
    path('', views.update_ticket, name='update_ticket'),
    path('search/', views.search_ticket, name='search_ticket'),
    path('success/', views.success, name='success'),
    path('list/', views.update_KA_json, name='update_KA_json'),
    path('search_ka_number/<ka_number>/', views.search_ka_number, name='search_ka_number')
]