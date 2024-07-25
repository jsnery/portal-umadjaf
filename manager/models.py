from django.db import models  # type: ignore


# Model para as congregações
class Congregations(models.Model):
    '''
    Model para as congregações

    Atributos:
        - name: Nome
        - address: Endereço
        - area: Área
    '''
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    area = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} ({self.area})'
