from django import forms
from .models import Booking, Provider, CustomUser, Review
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    location = forms.CharField(max_length=255, required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    user_type = forms.ChoiceField(choices=[('user', 'Regular User'), ('provider', 'Service Provider')])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'location', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def error_messages(self, field_name):
        return f"<div class='invalid-feedback'>{', '.join([str(msg) for msg in self.errors[field_name]])}</div>"

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['menu', 'date', 'message']

class ProviderSearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100)

class ProviderReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Assuming 'rating' and 'comment' are fields in your Review model

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating