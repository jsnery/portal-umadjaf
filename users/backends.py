from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


# Função de formatação de número de telefone
def format_number_phone(number_phone):
    '''
    Formatação de número de telefone

    Responsável por formatar o número de telefone do usuário
    do padrão (XX) XXXXX-XXXX para XXXXXXXXXXXX.

    Parâmetros:
        - number_phone: str

    Retorno:
        - str
    '''

    number = []
    for i in number_phone:
        if i.isdigit():
            number.append(i)

    return ''.join(number)


class NumberPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        number_phone = kwargs.get('number_phone', username)
        number_phone = format_number_phone(number_phone)
        try:
            user = UserModel.objects.get(number_phone=number_phone)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):  # type: ignore
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None