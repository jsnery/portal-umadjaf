from django.db import models  # type: ignore
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
class Roles(models.Model):
    '''
    Roles model

    Atibutos:

    role: str
    '''
    role = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.role}'


class User(AbstractBaseUser, PermissionsMixin):
    complete_name = models.CharField(max_length=100)
    number_phone = models.CharField(max_length=15, unique=True)
    birthday = models.DateField()
    church = models.CharField(max_length=100)
    is_umadjaf = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'number_phone'

    def __str__(self):
        return f'({self.id}) {self.complete_name}'

    def has_perm(self, perm, obj=None):
        """
        Retorna True se o usuário tiver a permissão especificada.
        """
        return self.is_active and (self.is_superuser or self.user_permissions.filter(codename=perm).exists())

    def has_module_perms(self, app_label):
        """
        Retorna True se o usuário tiver permissão para acessar modelos no aplicativo especificado.
        """
        return self.is_active and (self.is_superuser or self.user_permissions.filter(content_type__app_label=app_label).exists())


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
        upload_to='profiles/pictures/profiles_/',
        default='profiles/pictures/default.jpg'
    )
    bio = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id}'


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
        return f'{self.user_id} ({'Aprovado' if self.checked else 'Reprovado'})'
