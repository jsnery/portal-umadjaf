from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Upload de fotos de perfil
def get_upload_to_profiles(instance, filename):
    user_id = instance.user_id.id
    return f'users/profile_pictures/{user_id}/{user_id}.jpg'


# Permissões
class Roles(models.Model):
    '''
    Roles model

    Atibutos:

    role: str
    '''
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'({self.id}) {self.role}'  # type: ignore


# Usuário
class User(AbstractBaseUser, PermissionsMixin):
    '''
    O modelo User é uma classe abstrata que implementa a interface de usuário
    do Django. Dessa forma substituímos o modelo de usuário padrão do Django
    pelo nosso modelo de usuário personalizado.

    O modelo User em sim é independente, mas possui um relacionamento com os
    modelos UserRoles, UserProfiles e IsUmadjaf. Se o modelo User for apagado,
    os modelos UserRoles, UserProfiles e IsUmadjaf também serão apagados.

    Atibutos:
        - id: int (primary key)
        - complete_name: str
        - number_phone: str
        - birthday: date
        - church: str
        - is_umadjaf: bool
        - created_at: datetime
        - updated_at: datetime
        - last_login: datetime
        - is_staff: bool
        - is_superuser: bool
    '''
    complete_name = models.CharField(max_length=100)
    number_phone = models.CharField(max_length=15, unique=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ], default='M')
    church = models.CharField(max_length=100)
    is_umadjaf = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'number_phone'

    def __str__(self):
        return f'({self.id}) {self.complete_name}'  # type: ignore

    def has_perm(self, perm, obj=None):
        """
        Retorna True se o usuário tiver a permissão especificada.
        """
        return self.is_active and (
            self.is_superuser or self.user_permissions.filter(
                codename=perm).exists())

    def has_module_perms(self, app_label):
        """
        Retorna True se o usuário tiver permissão para acessar modelos
        no aplicativo especificado.
        """
        return self.is_active and (
            self.is_superuser or self.user_permissions.filter(
                content_type__app_label=app_label).exists())


# Permissões do usuário
class UserRoles(models.Model):
    '''
    UserRoles model

    Atibutos:

    user_id
    role_id
    created_at: datetime
    updated_at: datetime
    '''
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id} ({self.role_id})'


# Perfil do usuário
class UserProfiles(models.Model):
    '''
    UserProfiles model

    Atibutos:

    user_id: int
    bio: str
    updated_at: datetime
    '''
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=get_upload_to_profiles,
        default='users/profile_pictures/default.jpg'
    )
    bio = models.TextField(max_length=75)
    show_gallery = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id}'

    def save(self, *args, **kwargs):
        # Tenta excluir o arquivo antigo quando está sendo atualizado
        try:
            this = UserProfiles.objects.get(id=self.id)  # type: ignore
            if this.profile_picture != self.profile_picture:
                this.profile_picture.delete(save=False)
        except Exception:
            pass
        super(UserProfiles, self).save(*args, **kwargs)


# Aprovação de usuários
class IsUmadjaf(models.Model):
    '''
    IsUmadjaf model

    Atibutos:

    user_id: int
    checked: bool
    '''
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id} ({'approve' if self.checked else 'reprobate'})'
