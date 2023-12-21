from django.urls import path
from .views import (
    ProviderListView, ProviderDetailView,
    MenuListView, MenuDetailView,
    book_provider, booking_success, RegisterView, UserProfileView, custom_logout
)


urlpatterns = [
    path('', ProviderListView.as_view(), name='provider_list'),
    path('provider/<int:pk>/', ProviderDetailView.as_view(), name='provider_detail'),
    path('custom_logout/', custom_logout, name='custom_logout'),
    path('menus/', MenuListView.as_view(), name='menu_list'),
    path('menu/<int:pk>/', MenuDetailView.as_view(), name='menu_detail'),
    path('provider/<int:provider_id>/book/', book_provider, name='book_provider'),
    path('booking/success/', booking_success, name='booking_success'),
    path('register/', RegisterView.as_view(), name='register'),
    path('accounts/profile/', UserProfileView.as_view(), name='user_profile'),
]
