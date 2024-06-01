from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from profiles.models import User, UserRoles, Roles, IsUmadjaf
from .models import Congregations
from .forms import UserRolesForm, IsUmadjafForm, UserForm, CongregationForm


# Funções do novo painel de controle

def adm_panel(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')
    return render(
        request,
        'manager/pages/adm_panel.html',
        context={
            'is_authenticated': is_authenticated
        }
    )


# Funções de gerenciamento de usuários
def users(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if user_is_admin:
            return redirect('profiles:login')
    
    users = User.objects.all()  # Busca todos os usuários cadastrados
    roles = Roles.objects.all()  # Busca todos os cargos cadastrados
    return render(
        request,
        'manager/pages/users/users.html',
        context={
            'is_authenticated': is_authenticated,
            'users_all': users,
            'roles': roles
        }
    )


def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)  # Busca o usuário pelo ID
    user.delete()  # Deleta o usuário
    return HttpResponseRedirect(reverse('manager:users'))


def user_edit(request, user_id):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')
    user = User.objects.get(id=user_id)  # Busca o usuário pelo ID
    user_roles = UserRoles.objects.get(user_id=user_id)  # Busca o cargo do usuário pelo ID
    umadjaf = IsUmadjaf.objects.get(user_id=user_id)  # Busca se o usuário é umadjaf pelo ID

    print("Log: Usuário encontrado")
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        user_roles_form = UserRolesForm(request.POST, instance=user_roles)
        umadjaf_form = IsUmadjafForm(request.POST, instance=umadjaf)
        print("Log: Formulários recebidos")
        if user_form.is_valid() and user_roles_form.is_valid() and umadjaf_form.is_valid():
            print("Log: Formulários válidos")
            user_form.save()
            user_roles_form.save()
            umadjaf_form.save()
            return redirect('manager:users')  # Redireciona para a lista de usuários após a edição
    else:
        print("Log: Formulários não recebidos")
        user_form = UserForm(instance=user)
        user_roles_form = UserRolesForm(instance=user_roles)
        umadjaf_form = IsUmadjafForm(instance=umadjaf)

    return render(
        request,
        'manager/pages/users/partials/user_edit.html',
        context={
            'user_form': user_form,
            'user_roles_form': user_roles_form,
            'umadjaf_form': umadjaf_form
        }
    )


# Funções de gerenciamento de cargos
def users_roles(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')

    users_roles_all = UserRoles.objects.all()
    return render(
        request,
        'manager/pages/permissions/users_roles.html',
        context={
            'is_authenticated': is_authenticated,
            'users_roles_all': users_roles_all
        }
    )


def role_changer(request, user_id):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')

    user_role = UserRoles.objects.get(user_id=user_id)
    if request.method == 'POST':
        user_role_form = UserRolesForm(request.POST, instance=user_role)
        if user_role_form.is_valid():
            user_role_form.save()
            return redirect('manager:users_roles')
    else:
        user_role_form = UserRolesForm(instance=user_role)
    return render(
        request,
        'manager/pages/permissions/partials/role_changer.html',
        context={
            'user_role_form': user_role_form,
        }
    )


# Funções de gerenciamento de congregações
def congregations(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')

    congregations = Congregations.objects.all()
    return render(
        request,
        'manager/pages/congregations/congregation.html',
        context={
            'is_authenticated': is_authenticated,
            'congregations_all': congregations
        }
    )


def congregation_add(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')

    if request.method == 'POST':
        congregation = Congregations(
            name=request.POST['name'],
            address=request.POST['address'],
            area=request.POST['area']
        )
        congregation.save()
        return redirect('manager:congregations')
    return render(request, 'manager/pages/congregations/partials/congregation_add.html')


def congregation_edit(request, congregation_id):
    congregation = get_object_or_404(Congregations, pk=congregation_id)
    if request.method == 'POST':
        congregation_form = CongregationForm(request.POST, instance=congregation)
        if congregation_form.is_valid():
            congregation_form.save()
            return redirect('manager:congregations')
    else:
        congregation_form = CongregationForm(instance=congregation)
    return render(
        request,
        'manager/pages/congregations/partials/congregation_edit.html',
        context={
            'congregation_form': congregation_form
        }
    )


def congregation_delete(request, congregation_id):
    congregation = get_object_or_404(Congregations, pk=congregation_id)
    congregation.delete()
    return HttpResponseRedirect(reverse('manager:congregations'))


# Funções de gerenciamento de Membros
def members(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff and request.user.is_superuser # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('profiles:login')

    members = IsUmadjaf.objects.all()
    return render(
        request,
        'manager/pages/members/check.html',
        context={
            'is_authenticated': is_authenticated,
            'members_all': members
        }
    )


def member_positive(request, member_id):
    member = User.objects.get(id=member_id)
    umadjaf = IsUmadjaf.objects.get(user_id=member)

    member.is_umadjaf = False
    umadjaf.checked = True

    member.save()
    umadjaf.save()

    return HttpResponseRedirect(reverse('manager:members'))


def member_negative(request, member_id):
    print(member_id)
    member = User.objects.get(id=member_id)
    umadjaf = IsUmadjaf.objects.get(user_id=member)

    member.is_umadjaf = False
    umadjaf.checked = False

    member.save()
    umadjaf.save()

    return HttpResponseRedirect(reverse('manager:members'))
