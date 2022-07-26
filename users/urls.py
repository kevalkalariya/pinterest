from users import views as user_views
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import RegisterUser, LogoutUser, ProfileView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('view_profile/', user_views.ViewProfile.as_view(), name='view-profile'),
    path('view_profile/<str:board>/', user_views.ViewProfile.as_view(), name='add-board'),


    # reset password url
    path('password-change/', user_views.ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name="password_reset"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name="password_reset_complete"),
]
