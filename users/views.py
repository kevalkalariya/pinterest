from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from posts.models import PinBoards, Pin, SavePin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


class RegisterUser(View):
    """this class for register user and create there profile"""
    def get(self, request):
        form = SignUpForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        user_register = SignUpForm(request.POST)
        if user_register.is_valid():
            instance = user_register.save()
            profile_obj = Profile(user=instance)
            profile_obj.save()
            user_name = instance.temp_username  # For By defalut username
            instance.username = user_name
            instance.save()
            login(request, instance)
            messages.info(request, f'Your account has been created! Now you are able to login!!')
            return redirect('interest')
        # print(f"ERROR {user_register.errors}")
        return render(request, 'users/register.html', {'form': user_register})


class LogoutUser(View):
    """this class for logout user"""
    def get(self, request):
        logout(request)
        return redirect('login')


class ProfileView(View, LoginRequiredMixin):
    """this class for use profile update"""
    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=Profile.objects.get(user=request.user))
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Please Enter Valid input!')
            return redirect('profile')

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=Profile.objects.get(user=request.user))
        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form,
                                                      'profile_url': Profile.objects.get(user=request.user).image.url})


class ViewProfile(ListView):
    """this class for view profile"""
    def get(self, request, *args, **kwargs):
        boards = PinBoards.objects.filter(user_id_id=self.request.user)
        print('boards',boards)
        pins = Pin.objects.filter(author=self.request.user).order_by('-date_posted')
        print('pins',pins)
        savedpins = SavePin.objects.filter(user_id=request.user)
        context = {'boards': boards, 'pins': pins, 'savedpins': savedpins}
        return render(request, 'users/view_profile.html', context=context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    """this class for change the password"""
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
