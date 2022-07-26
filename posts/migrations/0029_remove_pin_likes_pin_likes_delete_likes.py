# Generated by Django 4.0.5 on 2022-07-19 11:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0028_followers_is_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pin',
            name='likes',
        ),
        migrations.AddField(
            model_name='pin',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Likes',
        ),
    ]
