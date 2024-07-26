from django.test import TestCase
from ..models import User
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
        User.objects.create(
            complete_name='John Doe',
            number_phone='(11) 94002-8922',
            birthday='1999-01-01',
            church='Test Church',
            is_umadjaf=True,
            is_staff=False,
            is_superuser=False
        )

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
