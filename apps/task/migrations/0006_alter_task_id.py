# Generated by Django 5.0.1 on 2024-02-01 22:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task", "0005_alter_task_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("024b436e-b35c-4587-bb08-57be1576d7a2"),
                editable=False,
                primary_key=True,
                serialize=False,
                verbose_name="task id",
            ),
        ),
    ]