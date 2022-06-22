from django.contrib import admin
from .models import Pin, PinCategory,UserInterest,PinBoard

# Register your models here.
admin.site.register(Pin)
admin.site.register(PinCategory)
admin.site.register(UserInterest)
admin.site.register(PinBoard)
