# Generated by Django 5.0.4 on 2024-04-25 01:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('complete_name', models.CharField(max_length=100)),
                ('number_phone', models.CharField(max_length=15)),
                ('birthday', models.DateField()),
                ('password', models.CharField(max_length=50)),
                ('church', models.CharField(max_length=100)),
                ('is_umadjaf', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('profile_picture', models.ImageField(default='profiles/default.jpg', upload_to='profiles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bio', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.roles')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.user')),
            ],
        ),
    ]