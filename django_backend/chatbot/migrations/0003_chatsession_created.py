# Generated by Django 5.1.7 on 2025-03-09 14:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0002_chatsession"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatsession",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
