# Generated by Django 4.2 on 2023-05-07 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseplatform', '0003_answer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
