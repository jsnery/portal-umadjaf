from functools import wraps
from users.models import UserRoles, Roles, IsUmadjaf


# Decorator para verificar se o usuário está autenticado e se é da equipe
def authenticated_user(view_func):
    '''
    Decorator para verificar se o usuário está autenticado e se é da equipe

    Este decorator verifica se o usuário está autenticado e se é um membro da
    equipe de mídia. Caso o usuário esteja autenticado, o decorator adiciona
    as seguintes variáveis ao contexto da view:
    - is_authenticated: Indica se o usuário está autenticado.
    - is_admin: Indica se o usuário é um administrador.
    - is_media_manager: Indica se o usuário é um gerente de mídia.
    - is_devotion_manager: Indica se o usuário é um gerente de devoções.
    - is_coordinator: Indica se o usuário é um coordenador.
    - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Parâmetros:
        - view_func: A função de view a ser decorada.

    Retorna:
        - A função de view decorada.
    '''
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            is_admin = request.user.is_staff  # type: ignore
            is_media_manager = UserRoles.objects.filter(
                user_id=request.user,
                role_id=Roles.objects.get(role='MediaManager')).exists()

            is_devotion_manager = UserRoles.objects.filter(
                user_id=request.user,
                role_id=Roles.objects.get(role='DevotionManager')).exists()

            is_coordinator = UserRoles.objects.filter(
                user_id=request.user,
                role_id=Roles.objects.get(role='Coordinator')).exists()

            is_umadjaf = IsUmadjaf.objects.get(
                user_id=request.user).checked
        else:
            is_admin = False
            is_media_manager = False
            is_devotion_manager = False
            is_coordinator = False
            is_umadjaf = False

        return view_func(request, *args, **kwargs,
                         is_authenticated=is_authenticated,
                         is_admin=is_admin,
                         is_media_manager=is_media_manager,
                         is_devotion_manager=is_devotion_manager,
                         is_coordinator=is_coordinator,
                         is_umadjaf=is_umadjaf
                         )

    return wrapper
