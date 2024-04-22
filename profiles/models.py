from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)  # name -> define o nome do usuário
    email = models.EmailField()  # email -> define o email do usuário
    password = models.CharField(max_length=50)  # password -> define a senha do usuário
    igreja = models.CharField(max_length=100)  # igreja -> define a igreja do usuário
    is_umadjaf = models.BooleanField(default=False)  # is_umadjaf -> define se o usuário é um membro da UMADJAF
    is_active = models.BooleanField(default=True)  # is_active -> define se o usuário está ativo
    is_staff = models.BooleanField(default=False)  # is_staff -> define se o usuário é um membro da equipe
    is_superuser = models.BooleanField(default=False)  # is_superuser -> define se o usuário é um superusuário
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True -> seta a data atual no momento da criação
    updated_at = models.DateTimeField(auto_now=True)  # auto_now=True -> seta a data atual no momento da atualização

    def __str__(self):
        return f'{self.name} - {self.igreja}'
