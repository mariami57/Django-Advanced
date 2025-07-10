from django.contrib.auth import get_user_model, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from accounts.forms import AppUserCreationForm

# Create your views here..
UserModel = get_user_model()

class RegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)

        if response.status_code in [301, 302]:
            login(self.request, self.object)

        return response

def login_view(request):
    return render(request, 'accounts/login-page.html')

def profile_details_view(request, pk:int):
    return render(request, 'accounts/profile-details-page.html')

def profile_edit_view(request, pk:int):
    return render(request, 'accounts/profile-edit-page.html')

def profile_delete_view(request, pk:int):
    return render(request, 'accounts/profile-delete-page.html')