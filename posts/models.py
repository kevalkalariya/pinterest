from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class PinCategory(models.Model):
    category_name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='profile_pics/', null=True)

    def __str__(self):
        return self.category_name


class Pin(models.Model):
    img = models.ImageField(upload_to='profile_pics/')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_category = models.ForeignKey(PinCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_cate = models.ForeignKey(PinCategory, on_delete=models.CASCADE)


class PinBoard(models.Model):
    board_name = models.CharField(max_length=100)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.board_name
