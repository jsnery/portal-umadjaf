from django import template  # type: ignore
from users.models import UserRoles, IsUmadjaf, User
from manager.models import Congregations

register = template.Library()  # Serve para registrar as funções abaixo


@register.simple_tag
def get_user_role(user_id):
    '''
    Serve para pegar o cargo do usuário pelo ID
    '''
    try:
        role = UserRoles.objects.get(user_id=user_id).role_id
    except UserRoles.DoesNotExist:
        role = 'DoesNotExist'
    return role


@register.simple_tag
def get_user_umadjaf(user_id):
    usuario = User.objects.get(id=user_id)
    try:
        umadjaf = IsUmadjaf.objects.get(user_id=user_id).checked
        if umadjaf:
            umadjaf = 'Sim'
        elif umadjaf is False and usuario.is_umadjaf is True:
            umadjaf = 'Aguardando'
        elif umadjaf is False:
            umadjaf = 'Não'
    except IsUmadjaf.DoesNotExist:
        umadjaf = 'Não'
    return umadjaf


@register.simple_tag
def return_verificated(booleando):
    if booleando:
        return 'Sim'
    return 'Aguardando'


@register.simple_tag
def return_church_name(church_id):
    try:
        church = Congregations.objects.get(id=church_id).name
    except IsUmadjaf.DoesNotExist:
        church = 'False'
    return church


@register.simple_tag
def return_user_name(user_id):
    try:
        user = User.objects.get(id=user_id).complete_name
    except User.DoesNotExist:
        user = 'Não Encontrado'
    return user