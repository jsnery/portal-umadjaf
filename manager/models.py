from django.db import models  # type: ignore


class Congregations(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    area = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} ({self.area})'
