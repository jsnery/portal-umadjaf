from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.http import JsonResponse
from users.models import IsUmadjaf, Roles, User, UserProfiles, UserRoles
from .forms import ProfileUsePictureForm, ProfileUserBioForm, ProfileUserForm, ProfileUserPassForm
from manager.models import Congregations
from articles.models import Articles

from utils.profiles.factory import make_fake_pedidos, make_fake_posts

pedidos = make_fake_pedidos()
post = make_fake_posts()


# Sistema de autenticação de usuário
def register(request):
    alert = False
    congregations = Congregations.objects.all()
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    if is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        is_umadjaf = request.POST['is_umadjaf'] == 'true'

        try:
            new_user = User(
                complete_name=request.POST['full_name'],
                number_phone=request.POST['number_phone'],
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
            user_id=new_user
        )

        new_profile.save()

        default_role = Roles.objects.get(role="Default")

        new_role = UserRoles(
            user_id=new_user,
            role_id=default_role
        )

        new_role.save()

        if is_umadjaf:
            new_umadjaf = IsUmadjaf(
                user_id=new_user
            )
        elif not is_umadjaf:
            new_umadjaf = IsUmadjaf(
                user_id=new_user,
                checked=False
            )

        new_umadjaf.save()

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


def login_(request):
    alert = False
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    if is_authenticated:
        return redirect('users:profile')
    if request.method == 'POST':
        number_phone = request.POST['number_phone']
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
def profile(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    user_is_coordinator = UserRoles.objects.filter(user_id=request.user.id, role_id=Roles.objects.get(role='Coordinator')).exists()

    # Bacos de dados
    posts = Articles.objects.filter(
        author_id=request.user.id
        ).order_by('-id')

    group_members = User.objects.filter(
        church=request.user.church,
        isumadjaf__checked=True
        )

    is_umadjaf = False
    if request.user.is_authenticated:
        user_id = request.user.id
        member_ok = IsUmadjaf.objects.filter(user_id=user_id).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=user_id).checked

    if is_authenticated:
        user = UserProfiles.objects.get(user_id=request.user.id)

        return render(
            request,
            'user_profile/pages/profile.html',
            context={
                'is_authenticated': request.user.is_authenticated,
                'is_admin': user_is_admin,
                'is_umadjaf': is_umadjaf,
                'is_coordinator': user_is_coordinator,
                'profile': user,  # Use a variável user diretamente
                'user': request.user,  # Use request.user diretamente
                'posts': posts,
                'group_members': group_members,
                'pedidos': pedidos
            }
        )
    else:
        return redirect('profiles:login')


def profile_settings(request):
    '''
    Profile settings

    Responsavel por gerar o formulário de configurações do perfil do usuário
    Ele permite que o usuário altere suas informações pessoais, senha e foto de perfil
    '''
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    if not is_authenticated:
        return redirect('users:login')

    user = User.objects.get(id=request.user.id)  # Pega o usuário logado
    user_profile = UserProfiles.objects.get(user_id=user.id)  # Pega o perfil do usuário logado

    # print(user)

    if request.method == 'POST':
        user_form = ProfileUserForm(request.POST, instance=user)  # Cria o formulário de usuário
        user_password_form = ProfileUserPassForm(request.POST, instance=user)  # Cria o formulário de senha
        user_profile_form = ProfileUserBioForm(request.POST, instance=user_profile)  # Cria o formulário de perfil
        user_picture_form = ProfileUsePictureForm(request.POST, request.FILES, instance=user_profile, label_suffix='')  # Cria o formulário de foto de perfil

        if user_form.is_valid() and user_profile_form.is_valid() and user_picture_form.is_valid():
            if user_password_form.is_valid():
                user_form.save()
                user_password_form.save()
                user_profile_form.save()
                user_picture_form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Houve um erro ao enviar o formulário.'})

    else:
        user_form = ProfileUserForm(instance=user)  # Cria o formulário de usuário
        user_password_form = ProfileUserPassForm(instance=user)  # Cria o formulário de senha
        user_profile_form = ProfileUserBioForm(instance=user_profile)  # Cria o formulário de perfil
        user_picture_form = ProfileUsePictureForm(instance=user_profile, label_suffix='')  # Cria o formulário de foto de perfil

    return render(
        request,
        'user_profile/pages/partials/partials/module_settings.html',
        context={
            'is_authenticated': is_authenticated,  # Faz a verificação se o usuário está logado
            'user_form': user_form,
            'user_password_form': user_password_form,
            'user_profile_form': user_profile_form,
            'user_picture_form': user_picture_form
        }
    )


def profile_logout(request):
    '''
    Profile logout

    Responsável por deslogar o usuário
    '''
    logout(request)
    return redirect('users:login')


# Funções de outro perfil
def other_profile(request, user_id):
    '''
    Other profile

    Responsável por gerar o perfil de outro usuário
    '''
    print(user_id)
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    user_is_admin = request.user.is_staff  # Verifica se o usuário é admin
    user_is_coordinator = UserRoles.objects.filter(user_id=request.user.id, role_id=Roles.objects.get(role='Coordinator')).exists()

    is_umadjaf = False
    if request.user.is_authenticated:
        user_id_ = request.user.id
        member_ok = IsUmadjaf.objects.filter(user_id=user_id_).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=user_id_).checked

    try:  # Tenta pegar o perfil do usuário
        profile = UserProfiles.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        posts = Articles.objects.filter(author_id=user_id).order_by('-id')
    except Exception:  # Se não conseguir, retorna um erro
        return redirect('users:profile_does_not_exists')

    return render(
        request,
        'other_profile/pages/other_profile.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': user_is_admin,
            'is_coordinator': user_is_coordinator,
            'is_umadjaf': is_umadjaf,
            'profile': profile,
            'user': user,
            'posts': posts,
        }
    )


def profile_does_not_exists(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    is_umadjaf = False
    if request.user.is_authenticated:
        user_id_ = request.user.id
        member_ok = IsUmadjaf.objects.filter(user_id=user_id_).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=user_id_).checked

    return render(
        request,
        'other_profile/pages/partials/profile_does_not_exists.html',
        context={
            'is_authenticated': is_authenticated,
            'is_umadjaf': is_umadjaf
        }
    )
