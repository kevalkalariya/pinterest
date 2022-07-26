# Generated by Django 4.0.5 on 2022-06-28 09:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_remove_comments_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]