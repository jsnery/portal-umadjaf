from django.test import TestCase
from ..models import User, UserProfiles
import datetime


# Testa se o usuário existe
class UserTestCase(TestCase):
    '''
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

    def setUp(self):
        new_user = User(
            complete_name='John Doe',
            number_phone='(11) 94002-8922',
            birthday='1999-01-01',
            church='Test Church',
            is_umadjaf=True,
            is_staff=False,
            is_superuser=False
        )

        new_user.set_password('123456')
        new_user.save()

    def test_user_exist(self):
        people = User.objects.get(complete_name='John Doe')
        self.assertEqual(people.complete_name, 'John Doe')
        self.assertEqual(people.number_phone, '(11) 94002-8922')
        self.assertEqual(people.birthday, datetime.date(1999, 1, 1))
        self.assertEqual(str(people.birthday), '1999-01-01')
        self.assertEqual(people.church, 'Test Church')
        self.assertEqual(people.is_umadjaf, True)
        self.assertEqual(people.is_staff, False)
        self.assertEqual(people.is_superuser, False)


class ProfileTestCase(TestCase):
    '''
    Atibutos:
        - id: int (primary key)
        - user_id: int
        - profile_picture: str | ImageField
        - bio: str
        - show_gallery: bool
        - updated_at: datetime
    '''

    def setUp(self):
        user = User(
            complete_name='John Doe',
            number_phone='(11) 94002-8923',
            birthday='1999-01-01',
            church='Test Church',
            is_umadjaf=True,
            is_staff=False,
            is_superuser=False
        )

        user.set_password('123456')
        user.save()

        UserProfiles.objects.create(
            user_id=user,
            bio='Test Bio'
        )

    def test_profile_exist(self):
        profile = UserProfiles.objects.get(bio='Test Bio')
        self.assertEqual(profile.user_id.complete_name, 'John Doe')
        self.assertEqual(profile.bio, 'Test Bio')
