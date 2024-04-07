from . import views
from . import api
from django.urls import path, include

urlpatterns = [
    path('', views.update_ticket, name='update_ticket'),
    path('success/', views.success, name='success'),
    path('list/', views.list_tickets_raw, name='list_tickets_raw'),
    path('search_ka_number/<ka_number>/', views.search_ka_number, name='search_ka_number')
]