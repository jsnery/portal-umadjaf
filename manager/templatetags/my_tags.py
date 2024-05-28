from django import template  # type: ignore
from profiles.models import UserRoles, IsUmadjaf, User

register = template.Library()


@register.simple_tag
def get_user_role(user_id):
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
