# Generated by Django 5.0.7 on 2024-07-22 18:35

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_userprofiles_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='profile_picture',
            field=models.ImageField(default='profiles/profile_pictures/default.jpg', upload_to=users.models.get_upload_to_profiles),
        ),
    ]
