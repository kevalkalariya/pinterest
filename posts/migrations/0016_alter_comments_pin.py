# Generated by Django 4.0.5 on 2022-06-28 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_rename_content_comments_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='pin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.pin'),
        ),
    ]
