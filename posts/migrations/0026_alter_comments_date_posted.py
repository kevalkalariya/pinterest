# Generated by Django 4.0.5 on 2022-06-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0025_alter_comments_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
