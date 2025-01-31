# Generated by Django 5.1.5 on 2025-01-31 10:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, max_length=2000)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
