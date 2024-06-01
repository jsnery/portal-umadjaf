from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.http import JsonResponse
from profiles.models import IsUmadjaf, Roles, User, UserProfiles, UserRoles
from utils.profiles.factory import make_fake_pedidos, make_fake_posts
from .forms import ProfileUsePictureForm, ProfileUserBioForm, ProfileUserForm, ProfileUserPassForm
from manager.models import Congregations
from articles.models import Article

pedidos = make_fake_pedidos()
post = make_fake_posts()


# Funções de cadastro e login
def register(request):
    congregations = Congregations.objects.all()
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    if is_authenticated:
        return redirect('profiles:profile')
    if request.method == 'POST':
        is_umadjaf = request.POST['is_umadjaf'] == 'true'

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

        return redirect('profiles:login')

    return render(
        request,
        'profiles/pages/register.html',
        context={
            'is_authenticated': is_authenticated,
            'congregations': congregations
        }
    )


def login_user(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    if is_authenticated:
        return redirect('profiles:profile')
    if request.method == 'POST':
        number_phone = request.POST['number_phone']
        password = request.POST['password']
        # user = User.objects.filter(number_phone=number_phone).first()
        user = authenticate(
            request, number_phone=number_phone, password=password)
        print("LOG 1: ", user)

        if user is not None:
            if check_password(password, user.password):
                login(request, user)  # type: ignore
                print('LOG 3: Logado')
                return redirect('profiles:profile')

    return render(
        request,
        'profiles/pages/login.html',
        context={
            'is_authenticated': is_authenticated,
        }
    )


# Funções de perfil
def profile(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    posts = Article.objects.filter(author=request.user.id)

    if is_authenticated:
        user = UserProfiles.objects.get(user_id=request.user.id)
        print(user)

        return render(
            request,
            'profiles/pages/profile.html',
            context={
                'is_authenticated': request.user.is_authenticated,
                'is_admin': user_is_admin,
                'profile': user,  # Use a variável user diretamente
                'user': request.user,  # Use request.user diretamente
                'posts': posts,
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
        return redirect('profiles:login')

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
        'profiles/pages/partials/profile_settings.html',
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
    return redirect('profiles:login')
