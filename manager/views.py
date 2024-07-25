from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from utils.decorators import authenticated_user
from users.models import IsUmadjaf, Roles, User, UserRoles
from .forms import (CongregationForm, IsUmadjafForm, UserForm, UserRolesForm)
from .models import Congregations


# Funções do novo painel de controle
@authenticated_user
def adm_panel(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    return render(
        request,
        'manager/pages/adm_panel.html',
        context={
            'is_authenticated': is_authenticated
        }
    )


# Funções de gerenciamento de usuários
@authenticated_user
def users(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

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


# Função remover usuário
@authenticated_user
def delete_user(request, user_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    if user_id == 1:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = get_object_or_404(User, pk=user_id)  # Busca o usuário pelo ID
    user.delete()  # Deleta o usuário
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Função editar usuário
@authenticated_user
def user_edit(request, user_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    user = User.objects.get(id=user_id)  # Busca o usuário pelo ID
    user_roles = UserRoles.objects.get(user_id=user_id)  # Busca o cargo do usuário pelo ID
    umadjaf = IsUmadjaf.objects.get(user_id=user_id)  # Busca se o usuário é umadjaf pelo ID

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        user_roles_form = UserRolesForm(request.POST, instance=user_roles)
        umadjaf_form = IsUmadjafForm(request.POST, instance=umadjaf)

        if user_form.is_valid() and user_roles_form.is_valid() and umadjaf_form.is_valid():

            if user_id == 1:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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


# Função de gerenciamento de cargos
@authenticated_user
def users_roles(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    users_roles_all = UserRoles.objects.all()
    return render(
        request,
        'manager/pages/permissions/users_roles.html',
        context={
            'is_authenticated': is_authenticated,
            'users_roles_all': users_roles_all
        }
    )


# Função de alteração de cargo
@authenticated_user
def role_changer(request, user_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    user_role = UserRoles.objects.get(user_id=user_id)
    if request.method == 'POST':
        user_role_form = UserRolesForm(request.POST, instance=user_role)
        if user_role_form.is_valid():
            if user_id == 1:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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


# Função de gerenciamento de congregações
@authenticated_user
def congregations(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    congregations = Congregations.objects.all()
    return render(
        request,
        'manager/pages/congregations/congregation.html',
        context={
            'is_authenticated': is_authenticated,
            'congregations_all': congregations
        }
    )


# Função de adicionar congregação
@authenticated_user
def congregation_add(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    if request.method == 'POST':
        congregation = Congregations(
            name=request.POST['name'],
            address=request.POST['address'],
            area=request.POST['area']
        )
        congregation.save()
        return redirect('manager:congregations')
    return render(request, 'manager/pages/congregations/partials/congregation_add.html')


# Função de editar congregação
@authenticated_user
def congregation_edit(request, congregation_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

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


# Função de deletar congregação
@authenticated_user
def congregation_delete(request, congregation_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    congregation = get_object_or_404(Congregations, pk=congregation_id)
    congregation.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Funções de gerenciamento de Membros
@authenticated_user
def members(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    members = IsUmadjaf.objects.all()
    return render(
        request,
        'manager/pages/members/check.html',
        context={
            'is_authenticated': is_authenticated,
            'members_all': members
        }
    )


# Função de aprovação de membro
@authenticated_user
def member_positive(request, member_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    member = User.objects.get(id=member_id)
    umadjaf = IsUmadjaf.objects.get(user_id=member)

    member.is_umadjaf = False
    umadjaf.checked = True

    if member_id == 1:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    member.save()
    umadjaf.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Função de reprovação de membro
@authenticated_user
def member_negative(request, member_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    member = User.objects.get(id=member_id)
    umadjaf = IsUmadjaf.objects.get(user_id=member)

    member.is_umadjaf = False
    umadjaf.checked = False

    if member_id == 1:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    member.save()
    umadjaf.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
