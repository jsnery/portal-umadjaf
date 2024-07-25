import os
from django.db import models


# Upload do banner do artigo
def get_upload_to_articles(instance, filename):
    return f'articles/{instance.at_created.strftime('%Y-%m-%d-%H-%M-%S')}/{filename}'


# Model de devocional
class Articles(models.Model):
    '''
    Model de artigos

    Atributos:
    - at_created: Data de criação do devocional
    - title: Título do devocional
    - versicle: Versículo do devocional
    - text: Texto do artigo
    - banner: Banner do devocional
    - author_id: ID do autor do devocional
    - is_official: Selinho Azul
    - post_unlock: Postagem desbloqueada (Para devocionais de não membros)
    '''
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

    # Deleta o banner do devocional ao deletar o devocional
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