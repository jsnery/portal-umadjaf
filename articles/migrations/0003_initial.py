# Generated by Django 5.0.7 on 2024-07-22 13:19

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0002_delete_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('versicle', models.CharField(default='', max_length=200)),
                ('text', models.TextField()),
                ('banner', models.ImageField(default='articles/default.jpg', upload_to=articles.models.get_upload_to_articles)),
                ('author_id', models.IntegerField(default=0)),
                ('is_official', models.BooleanField(default=False)),
            ],
        ),
    ]