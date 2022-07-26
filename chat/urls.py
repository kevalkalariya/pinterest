from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.ChatPage, name='user-chat'),
]
