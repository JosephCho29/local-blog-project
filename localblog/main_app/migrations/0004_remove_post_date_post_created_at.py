# Generated by Django 5.0.7 on 2024-07-25 16:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='date',
        ),
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
