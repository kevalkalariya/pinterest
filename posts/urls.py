from posts import views as post_views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PinListView, PinCreateView, PinDetailView, UserPinListView, PinUpdateView, interest_view, \
    BoardCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', PinListView.as_view(), name='home'),
    path('pin/new/', PinCreateView.as_view(), name='pin-create'),
    path('post/<int:pk>/update/', PinUpdateView.as_view(), name='pin-update'),
    # path('post/<int:pk>/delete/', PinDeleteView.as_view(), name='pin-delete'),
    path('user/posts/<int:pk>', UserPinListView.as_view(), name='user-pins'),
    path('post/<int:pk>/', PinDetailView.as_view(), name='pin-detail'),
    path('user/interest/', interest_view, name='interest'),
    path('board/new/', BoardCreateView.as_view(), name='board-create'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
