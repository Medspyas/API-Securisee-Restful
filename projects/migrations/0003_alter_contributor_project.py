# Generated by Django 5.1.5 on 2025-02-03 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributors",
                to="projects.project",
            ),
        ),
    ]
