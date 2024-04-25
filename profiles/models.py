from django.db import models  # type: ignore


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


class User(models.Model):
    '''
    User model

    Atibutos:

    complete_name: str
    number_phone: str
    birthday: date
    password: str
    church: str
    is_umadjaf: bool
    profile_picture: image
    created_at: datetime
    updated_at: datetime
    '''
    complete_name = models.CharField(max_length=100)
    number_phone = models.CharField(max_length=15, unique=True)
    birthday = models.DateField()
    password = models.CharField(max_length=50)
    church = models.CharField(max_length=100)
    is_umadjaf = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.id}) {self.complete_name}'


class UserRoles(models.Model):
    '''
    UserRoles model

    Atibutos:

    user_id: int
    role_id: int
    created_at: datetime
    updated_at: datetime
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    profule_picture = models.ImageField(
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
    is_umadjaf: bool
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id} ({'Aprovado' if self.checked else 'Reprovado'})'
