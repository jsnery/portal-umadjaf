from django.db import models  # type: ignore


# Create your models here.
class Roles(models.Model):
    '''
    Roles model

    Atibutos:

    role: str
    '''
    role = models.CharField(max_length=50)

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
    checked: bool
    profile_picture: image
    created_at: datetime
    updated_at: datetime
    '''
    complete_name = models.CharField(max_length=100)
    number_phone = models.CharField(max_length=15)
    birthday = models.DateField()
    password = models.CharField(max_length=50)
    church = models.CharField(max_length=100)
    is_umadjaf = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profiles/',
                                        default='profiles/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.igreja}'


class UserRoles(models.Model):
    '''
    UserRoles model

    Atibutos:

    user_id: int
    role_id: int
    created_at: datetime
    updated_at: datetime
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.role}'


class UserProfiles(models.Model):
    '''
    UserProfiles model

    Atibutos:

    user_id: int
    bio: str
    updated_at: datetime
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id}'
