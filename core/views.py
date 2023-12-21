from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Provider, Menu, CustomUser, Review
from .forms import BookingForm, ProviderSearchForm, ProviderReviewForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegistrationForm, ProviderForm
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg




class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        is_service_provider = form.cleaned_data['user_type'] == 'provider'

        if is_service_provider:
            with transaction.atomic():
                user = form.save()
                service_provider_form = ProviderForm(self.request.POST)
                if service_provider_form.is_valid():
                    service_provider = service_provider_form.save(commit=False)
                    service_provider.user = user
                    service_provider.save()
        else:
            return super().form_valid(form)

        return redirect(self.success_url)
    
def custom_logout(request):
    logout(request)
    return redirect('login')


class ProviderListView(ListView):
    model = Provider
    template_name = 'core/provider_list.html'
    context_object_name = 'providers'
    paginate_by = 10  # Pagination with 10 items per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply search filtering
        search_form = ProviderSearchForm(self.request.GET)
        if search_form.is_valid():
            queryset = queryset.filter(name__icontains=search_form.cleaned_data['q'])

        # Apply sorting options
        sort_option = self.request.GET.get('sort', None)
        if sort_option == 'name':
            queryset = queryset.order_by('name')
        elif sort_option == 'experience':
            queryset = queryset.order_by('-experience')
        elif sort_option == 'ratings':
            queryset = queryset.annotate(avg_ratings=Avg('reviews__rating')).order_by('-avg_ratings')

        # Apply additional filtering options (e.g., service type, location)
        # Adjust the field names and conditions based on your models

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProviderSearchForm()
        context['sort_option'] = self.request.GET.get('sort', 'default')

        # Add other context variables as needed
        return context

    def get_reviews(self, provider):
        # Retrieve and return reviews for a specific provider
        # You may need to adjust this based on your models
        return provider.reviews.all()

    def post(self, request, *args, **kwargs):
        # Handle form submission for leaving reviews
        # You may need to adjust this based on your models and forms
        provider_id = self.kwargs.get('pk')
        provider = Provider.objects.get(pk=provider_id)
        form = ProviderReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.provider = provider
            review.save()
            return HttpResponseRedirect(reverse('provider_detail', args=[provider_id]))

        return self.render_to_response(self.get_context_data(form=form))
    

class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'core/provider_detail.html'
    context_object_name = 'provider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch related menus
        context['menus'] = Menu.objects.filter(provider=self.object)

        # Fetch and calculate average rating of the provider
        context['average_rating'] = Review.objects.filter(provider=self.object).aggregate(Avg('rating'))['rating__avg']

        # Fetch reviews for the provider
        context['reviews'] = Review.objects.filter(provider=self.object)

        # Include the review form for users to submit new reviews
        context['review_form'] = ProviderReviewForm()

        return context

class MenuListView(ListView):
    model = Menu
    template_name = 'core/menu_list.html'
    context_object_name = 'menus'
    paginate_by = 10  # Pagination with 10 items per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filtering based on user's input (if applicable)
        return queryset.filter(provider__provider_type='Bartender')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Include additional context variables
        # For example, you might want to include provider information for each menu
        context['categories'] = Menu.objects.values_list('category', flat=True).distinct()

        return context


class MenuDetailView(DetailView):
    model = Menu
    template_name = 'core/menu_detail.html'
    context_object_name = 'menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Include additional context variables
        context['provider'] = self.object.provider
        context['reviews'] = self.object.reviews.all()
        context['average_rating'] = self.calculate_average_rating(context['reviews'])
        
        # Include related menus
        context['related_menus'] = Menu.objects.filter(provider=context['provider']).exclude(id=self.object.id)[:5]

        return context

    def calculate_average_rating(self, reviews):
        ratings = [review.rating for review in reviews]
        return sum(ratings) / len(ratings) if ratings else 0



def book_provider(request, provider_id):
    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Process the form data and create a booking
            # (customize this part based on your requirements)
            booking = form.save(commit=False)
            booking.provider = provider
            booking.user = request.user  # Assuming users are logged in
            booking.save()
            return redirect('booking_success')  # Redirect to a success page
    else:
        form = BookingForm()

    return render(request, 'core/book_provider.html', {'provider': provider, 'form': form})

def booking_success(request):
    return render(request, 'core/booking_success.html')

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user
