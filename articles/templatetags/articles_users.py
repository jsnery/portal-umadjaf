from django import template  # type: ignore
from users.models import User


register = template.Library()  # Serve para registrar as funções abaixo


@register.simple_tag
def return_user_name(user_id):
    try:
        user = User.objects.get(id=user_id).complete_name
    except User.DoesNotExist:
        user = "Usuário não encontrado"
    return user
