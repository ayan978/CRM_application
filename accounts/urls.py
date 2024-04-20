from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home),
    path('products/', views.products),
    path('customer/', views.customer),
]