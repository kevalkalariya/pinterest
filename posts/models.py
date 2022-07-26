import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# Create your models here.
class PinCategory(models.Model):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Pin(models.Model):
    img = models.ImageField(upload_to='profile_pics/',default='default.jpg',)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_category = models.ForeignKey(PinCategory, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_cate = models.ForeignKey(PinCategory, on_delete=models.CASCADE)


class PinBoards(models.Model):
    board_name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.board_name


class Boards(models.Model):
    board_id = models.ForeignKey(PinBoards, on_delete=models.CASCADE)
    pin_id = models.ForeignKey(Pin, on_delete=models.CASCADE, null=True)


class SavePin(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_id = models.ForeignKey(Pin, on_delete=models.CASCADE)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    comment = models.TextField(max_length=400)
    date_posted = models.DateTimeField(auto_now_add=True)


class Followers(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_follow = models.BooleanField(default=False)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)


