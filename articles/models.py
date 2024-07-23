import os
from django.db import models


def get_upload_to_articles(instance, filename):
    return f'articles/{instance.at_created.strftime('%Y-%m-%d-%H-%M-%S')}/{filename}'


class Articles(models.Model):
    at_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    versicle = models.CharField(max_length=200, default='')
    text = models.TextField()
    banner = models.ImageField(
        upload_to=get_upload_to_articles,
        default='articles/default.jpg'
    )
    author_id = models.IntegerField(default=0)
    is_official = models.BooleanField(default=False)
    post_unlock = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.banner:
            banner_path = self.banner.path
            if os.path.isfile(banner_path):
                os.remove(banner_path)
                banner_dir = os.path.dirname(banner_path)
                # Verifica se o diretório está vazio
                if not os.listdir(banner_dir):
                    os.rmdir(banner_dir)  # Remove o diretório se estiver vazio
        super(Articles, self).delete(*args, **kwargs)

    def __str__(self):
        return f'({self.id}) {self.title} ({self.at_created.strftime('%d/%m/%Y %H:%M')})'