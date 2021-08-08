from django.urls import path
from .views import (home_view, 
            SaleListView,
            SaleDetailsView)
app_name="sales"

urlpatterns = [
    path('', home_view, name='sales-home'),
    path('list/', SaleListView.as_view(), name='sale-list'),
    path('list/<int:pk>/', SaleDetailsView.as_view(), name='sale-details'),
]