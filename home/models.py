from django.db import models
import os
import time


# Upload das imagens para a pasta carrousel
def get_upload_to_carrousel(instance, filename):
    return f'carrousel/{instance.created.strftime('%Y-%m-%d-%H-%M-%S')}/{filename}'


# Model para o carrossel
class Carrousel(models.Model):
    '''
    Model para o carrossel

    Atributos:
    - created: Data de criação
    - title: Título
    - description: Descrição
    - image: Imagem
    - active: Ativo
    - author_id: ID do autor
    '''

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=get_upload_to_carrousel, default='carrousel/default.jpg')
    active = models.BooleanField(default=False)
    author_id = models.IntegerField(default=0)

    # Deletar a imagem do disco ao deletar o objeto
    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            try:
                os.remove(self.image.path)
            except PermissionError:
                time.sleep(1)  # Espera um pouco e tenta novamente
                try:
                    os.remove(self.image.path)
                except PermissionError as e:
                    # Loga o erro para análise posterior
                    print(f"Erro ao deletar o arquivo: {e}")

            directory = os.path.dirname(self.image.path)
            if not os.listdir(directory):
                try:
                    os.rmdir(directory)
                except OSError as e:
                    # Loga o erro se não conseguir remover o diretório
                    print(f"Erro ao remover o diretório: {e}")

        super().delete(*args, **kwargs)

    def __str__(self):
        return f'({self.id}) {self.title} - {self.created}'
