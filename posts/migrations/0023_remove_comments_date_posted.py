# Generated by Django 4.0.5 on 2022-06-28 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0022_comments_date_posted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='date_posted',
        ),
    ]
