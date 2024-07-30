from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from utils.decorators import authenticated_user
from django.http import JsonResponse
from manager.models import Congregations
from articles.models import Articles
from gallery.models import GalleryMarkedUser
from .models import IsUmadjaf, Roles, User, UserProfiles, UserRoles
from .forms import (
    ProfileUsePictureForm,
    ProfileUserBioForm,
    ProfileUserForm,
    ProfileUserPassForm
    )


'''
É utilizado o decorator @authenticated_user para verificar se o usuário está
autenticado.

Ele entrega os seguintes parâmetros para as views:
    - is_authenticated: Indica se o usuário está autenticado.
    - is_admin: Indica se o usuário é um administrador.
    - is_media_manager: Indica se o usuário é um gerente de mídia.
    - is_devotion_manager: Indica se o usuário é um gerente de devoções.
    - is_coordinator: Indica se o usuário é um coordenador.
    - is_umadjaf: Indica se o usuário é um membro da UMADJAF.
'''


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


# Sistema de cadastro de usuário
@authenticated_user
def register(request,
             is_authenticated,
             is_admin, is_media_manager,
             is_devotion_manager,
             is_coordinator,
             is_umadjaf
             ):
    '''
    Sistema de cadastro de usuário

    Responsável por cadastrar um novo usuário no sistema
    e redirecionar para a página de login.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorno:
        - HttpResponse (render)
    '''

    alert = False

    if is_authenticated:
        return redirect('users:profile')

    congregations = Congregations.objects.all()

    if request.method == 'POST':
        is_umadjaf = request.POST['is_umadjaf'] == 'true'
        number_phone = format_number_phone(request.POST['number_phone'])

        try:
            new_user = User(
                complete_name=request.POST['full_name'],
                number_phone=number_phone,
                birthday=request.POST['birth_date'],
                gender=request.POST['gender'],
                church=request.POST['church'],
                is_umadjaf=is_umadjaf,
            )
            new_user.set_password(request.POST['password'])

            new_user.save()

        except Exception:
            alert = True
            return render(
                request,
                'authentication/pages/register.html',
                context={
                    'is_authenticated': is_authenticated,
                    'alert': alert,
                    'congregations': congregations
                }
            )

        new_profile = UserProfiles(
            user_id=new_user,
            bio='O Senhor é o meu pastor; de nada terei falta.'
        )

        new_profile.save()

        default_role = Roles.objects.get(role="Default")

        new_role = UserRoles(
            user_id=new_user,
            role_id=default_role
        )

        new_role.save()

        umadjaf_check = IsUmadjaf(
            user_id=new_user
        )

        umadjaf_check.save()

        return redirect('users:login')

    return render(
        request,
        'authentication/pages/register.html',
        context={
            'is_authenticated': is_authenticated,
            'alert': alert,
            'congregations': congregations
        }
    )


# Sistema de login de usuário
@authenticated_user
def login_(request,
           is_authenticated,
           is_admin,
           is_media_manager,
           is_devotion_manager,
           is_coordinator,
           is_umadjaf
           ):
    '''
    Sistema de login de usuário

    Responsável por logar um usuário no sistema
    e redirecionar para a página de perfil.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorno:
        - HttpResponse (render)'''

    alert = False

    if is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        number_phone = format_number_phone(request.POST['number_phone'])
        password = request.POST['password']
        # user = User.objects.filter(number_phone=number_phone).first()
        user = authenticate(
            request, number_phone=number_phone, password=password)

        if user is not None:
            if check_password(password, user.password):
                login(request, user)  # type: ignore
                return redirect('users:profile')
        else:
            alert = True

    return render(
        request,
        'authentication/pages/login.html',
        context={
            'is_authenticated': is_authenticated,
            'alert': alert
        }
    )


# Funções de perfil do usuário logado
@authenticated_user
def profile(request,
            is_authenticated,
            is_admin,
            is_media_manager,
            is_devotion_manager,
            is_coordinator,
            is_umadjaf
            ):
    '''
    Perfil do usuário logado

    Responsável por mostrar o perfil do usuário logado
    e redirecionar para a página de login.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorno:
        - HttpResponse (render)
    '''

    if not is_authenticated:
        return redirect('users:login')

    user_id = request.user.id
    posts = Articles.objects.filter(
        author_id=user_id
        ).order_by('-id')

    group_members = User.objects.filter(
        church=request.user.church,
        isumadjaf__checked=True
        ).exclude(id=user_id)

    gallery = GalleryMarkedUser.objects.filter(
        user_id=user_id).filter(marked_confirm=True)

    user_profile = UserProfiles.objects.get(user_id=user_id)

    return render(
        request,
        'user_profile/pages/profile.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_umadjaf': is_umadjaf,
            'is_coordinator': is_coordinator,
            'profile': user_profile,
            'user': request.user,
            'posts': posts,
            'group_members': group_members,
            'gallery': gallery,
        }
    )


# Funções de edição de perfil
@authenticated_user
def profile_settings(request,
                     is_authenticated,
                     is_admin,
                     is_media_manager,
                     is_devotion_manager,
                     is_coordinator,
                     is_umadjaf
                     ):
    '''
    Edição de perfil

    Responsável por editar o perfil do usuário logado

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorno:
        - HttpResponse (render)
    '''

    if not is_authenticated:
        return redirect('users:login')

    user = request.user
    # Pega o perfil do usuário logado
    user_profile = UserProfiles.objects.get(user_id=user)

    # print(user)

    if request.method == 'POST':
        # Cria o formulário de usuário
        user_form = ProfileUserForm(request.POST, instance=user)
        # Cria o formulário de senha
        user_password_form = ProfileUserPassForm(request.POST, instance=user)
        # Cria o formulário de perfil
        user_profile_form = ProfileUserBioForm(
            request.POST,
            instance=user_profile
            )
        # Cria o formulário de foto de perfil
        user_picture_form = ProfileUsePictureForm(
            request.POST,
            request.FILES,
            instance=user_profile,
            label_suffix=''
            )

        if user_form.is_valid() \
                and user_profile_form.is_valid() \
                and user_picture_form.is_valid():

            if user_password_form.is_valid():
                user_form.save()
                user_password_form.save()
                user_profile_form.save()
                user_picture_form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})

    else:
        # Cria o formulário de usuário
        user_form = ProfileUserForm(instance=user)
        # Cria o formulário de senha
        user_password_form = ProfileUserPassForm(instance=user)
        # Cria o formulário de perfil
        user_profile_form = ProfileUserBioForm(instance=user_profile)
        # Cria o formulário de foto de perfil
        user_picture_form = ProfileUsePictureForm(
            instance=user_profile, label_suffix='')

    return render(
        request,
        'user_profile/pages/partials/partials/module_settings.html',
        context={
            'is_authenticated': is_authenticated,
            'user_form': user_form,
            'user_password_form': user_password_form,
            'user_profile_form': user_profile_form,
            'user_picture_form': user_picture_form
        }
    )


# Função de logout
def profile_logout(request):
    '''
    Logout do usuário

    Responsável por deslogar o usuário do sistema

    Parâmetros:
        - request: A requisição HTTP recebida.

    Retorno:
        - HttpResponse (redirect)
    '''

    logout(request)
    return redirect('users:login')


# Funções de outro perfil
@authenticated_user
def other_profile(request, other_user_id,
                  is_authenticated,
                  is_admin,
                  is_media_manager,
                  is_devotion_manager,
                  is_coordinator,
                  is_umadjaf
                  ):
    '''
    Perfil de outro usuário

    Responsável por mostrar o perfil de outro usuário

    Parâmetros:
        - request: A requisição HTTP recebida.
        - other_user_id: O ID do usuário a ser exibido.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorno:
        - HttpResponse (render)
    '''

    gallery = GalleryMarkedUser.objects.filter(
        user_id=other_user_id).filter(marked_confirm=True)

    try:  # Tenta pegar o perfil do usuário
        profile = UserProfiles.objects.get(user_id=other_user_id)
        user = User.objects.get(id=other_user_id)

        posts = Articles.objects.filter(
            author_id=other_user_id).order_by('-id')

        is_umadjaf = IsUmadjaf.objects.get(user_id=other_user_id).checked

    except Exception:  # Se não conseguir, retorna um erro
        return redirect('users:profile_does_not_exists')

    return render(
        request,
        'other_profile/pages/other_profile.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_umadjaf': is_umadjaf,
            'profile': profile,
            'user': user,
            'posts': posts,
            'gallery': gallery,
        }
    )


# Função de perfil não encontrado
@authenticated_user
def profile_does_not_exists(request,
                            is_authenticated,
                            is_admin,
                            is_media_manager,
                            is_devotion_manager,
                            is_coordinator,
                            is_umadjaf
                            ):
    '''
    Perfil não encontrado

    Responsável por mostrar a página de perfil não encontrado

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorno:
        - HttpResponse (render)
    '''

    return render(
        request,
        'other_profile/pages/profile_does_not_exists.html',
        context={
            'is_authenticated': is_authenticated
        }
    )
