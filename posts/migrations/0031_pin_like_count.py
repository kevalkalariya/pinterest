# Generated by Django 4.0.5 on 2022-07-20 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0030_remove_pin_likes_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]
