from django.urls import path, include
from .views import PinListView, PinCreateView, PinDetailView, UserPinListView, PinUpdateView, GetInterest, \
    BoardCreateView, SavePinProfile, SaveToBoard, ViewBoardPin, SearchPin, LikeView, PostFollowView, \
    PostUnfollowView, download_image, DeletePin, DateViewContent, InterestViewContent, ViewInterest, AddInterest, \
    DeleteInterest
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', PinListView.as_view(), name='home'),
    path('search/', SearchPin.as_view(), name='search'),
    path('pin/new/', PinCreateView.as_view(), name='pin-create'),
    path('post/<int:pk>/update/', PinUpdateView.as_view(), name='pin-update'),
    path('user/posts/<int:pk>', UserPinListView.as_view(), name='user-pins'),
    path('post/<int:pk>/', PinDetailView.as_view(), name='pin-detail'),
    path('user/interest/', GetInterest.as_view(), name='interest'),
    path('board/new/', BoardCreateView.as_view(), name='board-create'),
    path('pin/save/<int:pk>', SavePinProfile.as_view(), name='save-pin'),
    path('save/<str:board_name>/<int:pk>/', SaveToBoard.as_view(), name='dropdown-board'),
    path('user/view_profile/<str:board_name>/', ViewBoardPin.as_view(), name='view-board-pin'),
    path('like/', LikeView.as_view(), name='pin-like'),
    path('get_author_id/', PostUnfollowView.as_view(), name='post-unfollow'),
    path('author_follow_id/', PostFollowView.as_view(), name='post-follow'),
    path('download/<int:id>/', download_image, name='download-pin'),
    path('delete/<int:id>/', DeletePin.as_view(), name='delete-pin'),
    path('datawise_content/', DateViewContent.as_view(), name='datawise_content'),
    path('interestwise_content/', InterestViewContent.as_view(), name='interestwise_content'),

    path('view-interest/', ViewInterest.as_view(), name='view-interest'),
    path('add-interest/<int:id>/', AddInterest.as_view(), name='add-interest'),
    path('delete-interest/<int:id>/', DeleteInterest.as_view(), name='delete-interest'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
