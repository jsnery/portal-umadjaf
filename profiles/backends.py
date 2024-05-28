from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class NumberPhoneBackend(ModelBackend):
    def authenticate(self, request, number_phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(number_phone=number_phone)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None