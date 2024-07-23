from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from users.models import IsUmadjaf, Roles, User, UserRoles
from .forms import (CalendarForm, CongregationForm, IsUmadjafForm, UserForm,
                    UserRolesForm)
from .models import Congregations
from events.models import Event
from articles.models import Articles


# Funções do novo painel de controle
def adm_panel(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')
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
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if user_is_admin:
            return redirect('users:login')
    
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
    if user_id == 1:
        return HttpResponseRedirect(reverse('manager:users'))
    
    user = get_object_or_404(User, pk=user_id)  # Busca o usuário pelo ID
    user.delete()  # Deleta o usuário
    return HttpResponseRedirect(reverse('manager:users'))


def user_edit(request, user_id):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')
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
            if user_id == 1:
                return HttpResponseRedirect(reverse('manager:users'))
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
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

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
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

    user_role = UserRoles.objects.get(user_id=user_id)
    if request.method == 'POST':
        user_role_form = UserRolesForm(request.POST, instance=user_role)
        if user_role_form.is_valid():
            if user_id == 1:
                return HttpResponseRedirect(reverse('manager:users_roles'))
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
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

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
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

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
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

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

    if member_id == 1:
        return HttpResponseRedirect(reverse('manager:members'))

    member.save()
    umadjaf.save()

    return HttpResponseRedirect(reverse('manager:members'))


def member_negative(request, member_id):
    member = User.objects.get(id=member_id)
    umadjaf = IsUmadjaf.objects.get(user_id=member)

    member.is_umadjaf = False
    umadjaf.checked = False

    if member_id == 1:
        return HttpResponseRedirect(reverse('manager:members'))

    member.save()
    umadjaf.save()

    return HttpResponseRedirect(reverse('manager:members'))


# Sistema de calendário
def calendar(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

    calendar = Event.objects.all()

    return render(
        request,
        'manager/pages/calendar/calendar.html',
        context={
            'is_authenticated': is_authenticated,
            'calendar_all': calendar
        }
    )


def calendar_edit(request, calendar_id):
    calendar = get_object_or_404(Event, pk=calendar_id)
    event_logo = calendar.logo
    event_background = calendar.background
    if request.method == 'POST':
        calendar_edit_form = CalendarForm(request.POST, request.FILES, instance=calendar)
        if calendar_edit_form.is_valid():
            # O objeto 'calendar' será atualizado com os dados do formulário
            calendar_edit_form.save()
            return redirect('manager:calendar')
    else:
        calendar_edit_form = CalendarForm(instance=calendar)

    return render(
        request,
        'manager/pages/calendar/partials/calendar_edit.html',
        context={
            'calendar_edit_form': calendar_edit_form,
            'calendar_id': calendar_id,
            'event_logo': event_logo,
            'event_background': event_background
        }
    )


def calendar_delete(request, calendar_id):
    calendar = get_object_or_404(Event, pk=calendar_id)
    calendar.delete()
    return HttpResponseRedirect(reverse('manager:calendar'))


# Funções de gerenciamento de Artigos
def articles(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    articles = Articles.objects.all()

    if not is_authenticated:  # Se não estiver autenticado, redireciona para a página de login
        if not user_is_admin:
            return redirect('users:login')

    return render(
        request,
        'manager/pages/articles/articles.html',
        context={
            'is_authenticated': is_authenticated,
            'articles_all': articles
        }
    )


def article_verify(request, article_id):
    article = Articles.objects.get(id=article_id)
    article.is_official = True
    article.post_unlock = True
    article.save()
    return HttpResponseRedirect(reverse('manager:articles'))


def article_unverify(request, article_id):
    article = Articles.objects.get(id=article_id)
    article.is_official = False
    article.post_unlock = False
    article.save()
    return HttpResponseRedirect(reverse('manager:articles'))


def article_delete(request, article_id):
    article = get_object_or_404(Articles, pk=article_id)
    article.delete()
    return HttpResponseRedirect(reverse('manager:articles'))
