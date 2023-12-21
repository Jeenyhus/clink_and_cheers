from django.contrib import admin
from .models import UserProfile, Provider, Menu, Booking

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'menu', 'date', 'status')
