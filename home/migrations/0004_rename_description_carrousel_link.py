# Generated by Django 5.0.7 on 2024-07-30 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_delete_nada'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carrousel',
            old_name='description',
            new_name='link',
        ),
    ]
