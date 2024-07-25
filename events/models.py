import os
from django.db import models
from manager.models import Congregations


# Upload de imagens para o banner do evento
def get_upload_to_calendar(instance, filename):
    return f'events/{instance.date}/{filename}'


# Modelo de eventos
class Event(models.Model):
    '''
    Modelo de eventos

    Atributos:
        title (str): Título do evento
        date (date): Data do evento
        hours (time): Horário do evento
        theme (str): Tema do evento
        is_general (bool): Se é evento geral
        congregation (int): Congregação do evento
        logo (image): Logo do evento
        background (image): Imagem de fundo do evento
        author_id (int): ID do autor do evento
    '''
    title = models.CharField(max_length=200)
    date = models.DateField()
    hours = models.TimeField()
    theme = models.TextField(default='')
    is_general = models.BooleanField(default=False)
    congregation = models.ForeignKey(Congregations, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to=get_upload_to_calendar,
        default='events/default.jpg'
    )
    background = models.ImageField(
        upload_to=get_upload_to_calendar,
        default='events/default.jpg'
    )
    author_id = models.IntegerField(default=0)

    # Deletar imagens do evento ao deletar o evento
    def delete(self, *args, **kwargs):
        directories_to_check = set()

        if self.logo and os.path.isfile(self.logo.path):
            os.remove(self.logo.path)
            directories_to_check.add(os.path.dirname(self.logo.path))

        if self.background and os.path.isfile(self.background.path):
            os.remove(self.background.path)
            directories_to_check.add(os.path.dirname(self.background.path))

        for directory in directories_to_check:
            if not os.listdir(directory):
                os.rmdir(directory)

        super(Event, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.date})'
