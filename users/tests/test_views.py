from django.test import TestCase
from django.urls import reverse


# Testa se a view de registro de usuário está funcionando
class UserViewTestCase(TestCase):

    def test_user_register_code_200(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)


# Testa se a view de login de usuário está funcionando
class LoginViewTestCase(TestCase):

    def test_user_login_code_200(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
