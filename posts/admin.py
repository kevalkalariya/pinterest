from django.contrib import admin
from .models import Pin, PinCategory, UserInterest, PinBoards, Boards, SavePin, Comments, Followers, Likes

# Register your models here.
admin.site.register(Pin)
admin.site.register(PinCategory)
admin.site.register(UserInterest)
admin.site.register(PinBoards)
admin.site.register(Boards)
admin.site.register(SavePin)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Followers)
