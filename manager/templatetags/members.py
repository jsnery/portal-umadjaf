from django import template  # type: ignore
from profiles.models import UserRoles, IsUmadjaf, User
from manager.models import Congregations

register = template.Library()  # Serve para registrar as funções abaixo


@register.simple_tag
def return_umadjaf_status(member_id):
    usuario = User.objects.get(id=member_id.id)
    try:
        umadjaf = IsUmadjaf.objects.get(user_id=member_id).checked
        if umadjaf:
            umadjaf = 'Verificado'
        elif umadjaf is False and usuario.is_umadjaf is True:
            umadjaf = 'Aguardando'
        elif umadjaf is False:
            umadjaf = 'Não'
    except IsUmadjaf.DoesNotExist:
        umadjaf = 'Não'
    return umadjaf


@register.simple_tag
def return_church_name(member_id):
    try:
        church_id = User.objects.get(id=member_id.id).church
        church = Congregations.objects.get(id=church_id).name
    except IsUmadjaf.DoesNotExist:
        church = 'False'
    return church


@register.simple_tag
def return_member_name(member_id):
    try:
        member = User.objects.get(id=member_id.id).complete_name
    except IsUmadjaf.DoesNotExist:
        member = 'False'
    return member


@register.simple_tag
def return_member_id(member_id):
    try:
        member = User.objects.get(id=member_id.id).id
    except IsUmadjaf.DoesNotExist:
        member = 'False'
    return member


@register.simple_tag
def return_member_gender(member_id):
    try:
        member = User.objects.get(id=member_id.id).gender
        if member == 'M':
            member = 'Masculino'
        else:
            member = 'Feminino'
    except IsUmadjaf.DoesNotExist:
        member = 'False'
    return member
