from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.stock, name='stock'),

    path('stock-autocomplete/', views.StockAutocomplete.as_view(), name="stock_autocomplete"),
    path('stock-detail/<int:pk>/', views.stockdetail, name="stock_detail"),
]