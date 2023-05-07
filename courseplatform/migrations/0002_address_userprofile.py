# Generated by Django 4.2 on 2023-05-07 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseplatform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('detail_address', models.TextField(blank=True, max_length=2000, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('zip', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='courseplatform.address')),
                ('phone_number', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='courseplatform.user')),
            ],
            options={
                'abstract': False,
            },
            bases=('courseplatform.address',),
        ),
    ]