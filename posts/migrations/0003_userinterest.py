# Generated by Django 4.0.5 on 2022-06-21 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_pincategory_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin_cate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.pincategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
