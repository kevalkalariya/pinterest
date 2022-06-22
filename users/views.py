from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.views.generic import CreateView
from posts.models import PinBoard,Pin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
# class register(CreateView):
#     form_class = SignUpForm()
#     success_url = reverse_lazy('login')
#     template_name = 'users/register.html'


def register(request):
    user_register = SignUpForm()
    if request.method == 'POST':
        user_register = SignUpForm(request.POST)
        if user_register.is_valid():
            instance = user_register.save()
            profile_obj = Profile(user=instance)
            profile_obj.save()
            login(request, instance)
            messages.info(request, f'Your account has been created! Now you are able to login!!')
            return redirect('interest')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': user_register})


#
# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST.get('email').lower()
#         password = request.POST.get('password')
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username or password is incorrect !')
#     context = {}
#     return render(request, 'users/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'users/home.html')


@login_required
def profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please Enter Valid input!')
            return redirect('profile')

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class ViewProfile(ListView):
    template_name = 'users/view_profile.html'
    model = PinBoard
    context_object_name = 'boards'

    def get_queryset(self):
        print(PinBoard.objects.filter(pin__author=self.request.user))
        return PinBoard.objects.filter(pin__author=self.request.user)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
