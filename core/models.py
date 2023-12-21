from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Provider(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    skills = models.CharField(max_length=255)
    portfolio = models.CharField(max_length=255, blank=True, null=True)
    experience = models.PositiveIntegerField()
    profile_picture = models.ImageField(upload_to='provider_profiles/', null=True, blank=True)

    PROVIDER_TYPES = [
        ('Bartender', 'Bartender'),
        ('Chef', 'Chef'),
    ]

    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class Menu(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='menus')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateField()
    message = models.TextField()
    status_choices = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.provider.name} - {self.date}"

class Review(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.provider.name}"