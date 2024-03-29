# Generated by Django 4.2.10 on 2024-02-09 13:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("d15458ec-87a9-4d06-a14c-f88c8b150751"),
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="user id",
            ),
        ),
    ]
