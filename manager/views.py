from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from utils.decorators import authenticated_user
from users.models import IsUmadjaf, Roles, User, UserRoles
from .forms import (CongregationForm, IsUmadjafForm, UserForm, UserRolesForm)
from .models import Congregations
from django.core.paginator import Paginator


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

# Funções de gerenciamento de usuários
@authenticated_user
def users(request,
          is_authenticated,
          is_admin,
          is_media_manager,
          is_devotion_manager,
          is_coordinator,
          is_umadjaf
          ):
    '''
    Página de gerenciamento de usuários

    Esta view renderiza a página de gerenciamento de usuários do site. A página
    exibe uma lista com todos os usuários cadastrados no site, bem como os cargos
    de cada usuário.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de gerenciamento de usuários.
    '''

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    users = User.objects.all().order_by('-id')  # Busca todos os usuários cadastrados
    roles = Roles.objects.all()  # Busca todos os cargos cadastrados
    congregations = Congregations.objects.all()

    users_paginator = Paginator(users, 10)  # 8 artigos por página
    page_number = request.GET.get('page')  # Página atual
    page_users = users_paginator.get_page(page_number)

    return render(
        request,
        'manager/pages/users/users.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'users_all': page_users,
            'roles': roles,
            'congregations': congregations
        }
    )


@authenticated_user
def search_users(request,
                 is_authenticated,
                 is_admin,
                 is_media_manager,
                 is_devotion_manager,
                 is_coordinator,
                 is_umadjaf
                 ):

    users = User.objects.all().order_by('-id')
    congregations = Congregations.objects.all()
    roles = Roles.objects.all()

    areas = {
        '0': '--',
        '1': 'Área 1',
        '2': 'Área 2',
        '3': 'Área 3',
    }

    area = request.GET.get('areaSelect')
    congregation = request.GET.get('congregationSelect')
    if congregation:
        cong = Congregations.objects.get(id=congregation)
        users = users.filter(church=cong.id)

    elif area:
        area = areas[area]
        cong = Congregations.objects.filter(area=area)
        cong_id = [str(i['id']) for i in cong.values()]
        for user in users:
            if user.church not in cong_id:
                users = users.exclude(id=user.id)

    else:
        redirect('manager:users')

    users_paginator = Paginator(users, 10)  # 8 artigos por página
    page_number = request.GET.get('page')  # Página atual
    page_users = users_paginator.get_page(page_number)

    return render(
        request, 'manager/pages/users/users.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'users_all': page_users,
            'roles': roles,
            'congregations': congregations
        }
    )


# Função remover usuário
@authenticated_user
def delete_user(request, user_id,
                is_authenticated,
                is_admin,
                is_media_manager,
                is_devotion_manager,
                is_coordinator,
                is_umadjaf):
    '''
    Função para remover um usuário

    Esta view remove um usuário do banco de dados. A view recebe o ID do usuário
    a ser removido e o remove do banco de dados.

    Parâmetros:
        - request: Requisição HTTP.
        - user_id: ID do usuário a ser removido.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Redireciona o usuário para a página anterior.
    '''

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
def user_edit(request, user_id,
              is_authenticated,
              is_admin,
              is_media_manager,
              is_devotion_manager,
              is_coordinator,
              is_umadjaf):
    '''
    Função para editar um usuário

    Esta view edita um usuário no banco de dados. A view recebe o ID do usuário
    a ser editado e os dados do usuário são carregados em um formulário para
    edição.

    Parâmetros:
        - request: Requisição HTTP.
        - user_id: ID do usuário a ser editado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com o formulário de edição de usuário.
    '''

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
def users_roles(request,
                is_authenticated,
                is_admin,
                is_media_manager,
                is_devotion_manager,
                is_coordinator,
                is_umadjaf
                ):
    '''
    Página de gerenciamento de cargos

    Esta view renderiza a página de gerenciamento de cargos do site. A página
    exibe uma lista com todos os cargos cadastrados no site.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de gerenciamento de cargos.
    '''

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
            'is_admin': is_admin,
            'users_roles_all': users_roles_all
        }
    )


# Função de alteração de cargo
@authenticated_user
def role_changer(request, user_id,
                 is_authenticated,
                 is_admin,
                 is_media_manager,
                 is_devotion_manager,
                 is_coordinator,
                 is_umadjaf
                 ):
    '''
    Função para alterar o cargo de um usuário

    Esta view altera o cargo de um usuário no banco de dados. A view recebe o ID
    do usuário e carrega o cargo do usuário em um formulário para edição.

    Parâmetros:
        - request: Requisição HTTP.
        - user_id: ID do usuário a ter o cargo alterado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com o formulário de edição de cargo.
    '''

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
def congregations(request,
                  is_authenticated,
                  is_admin,
                  is_media_manager,
                  is_devotion_manager,
                  is_coordinator,
                  is_umadjaf
                  ):
    '''
    Página de gerenciamento de congregações

    Esta view renderiza a página de gerenciamento de congregações do site. A página
    exibe uma lista com todas as congregações cadastradas no site.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de gerenciamento de congregações.
    '''

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
            'is_admin': is_admin,
            'congregations_all': congregations
        }
    )


# Função de adicionar congregação
@authenticated_user
def congregation_add(request,
                     is_authenticated,
                     is_admin,
                     is_media_manager,
                     is_devotion_manager,
                     is_coordinator,
                     is_umadjaf
                     ):
    '''
    Função para adicionar uma congregação

    Esta view adiciona uma nova congregação ao banco de dados. A view recebe os
    dados da congregação a ser adicionada e salva a nova congregação no banco de
    dados.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Redireciona o usuário para a página de gerenciamento de congregações.
    '''

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
def congregation_edit(request, congregation_id,
                      is_authenticated,
                      is_admin,
                      is_media_manager,
                      is_devotion_manager,
                      is_coordinator,
                      is_umadjaf
                      ):
    '''
    Função para editar uma congregação

    Esta view edita uma congregação no banco de dados. A view recebe o ID da
    congregação a ser editada e os dados da congregação são carregados em um
    formulário para edição.

    Parâmetros:
        - request: Requisição HTTP.
        - congregation_id: ID da congregação a ser editada.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com o formulário de edição de congregação.
    '''

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
def congregation_delete(request, congregation_id,
                        is_authenticated,
                        is_admin,
                        is_media_manager,
                        is_devotion_manager,
                        is_coordinator,
                        is_umadjaf
                        ):
    '''
    Função para deletar uma congregação

    Esta view deleta uma congregação do banco de dados. A view recebe o ID da
    congregação a ser deletada e a deleta do banco de dados.

    Parâmetros:
        - request: Requisição HTTP.
        - congregation_id: ID da congregação a ser deletada.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Redireciona o usuário para a página anterior.
    '''

    if not is_authenticated:
        return redirect('login')

    if not is_admin:
        return redirect('home')

    congregation = get_object_or_404(Congregations, pk=congregation_id)
    congregation.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Funções de gerenciamento de Membros
@authenticated_user
def members(request,
            is_authenticated,
            is_admin,
            is_media_manager,
            is_devotion_manager,
            is_coordinator,
            is_umadjaf
            ):
    '''
    Página de gerenciamento de membros

    Esta view renderiza a página de gerenciamento de membros da UMADJAF. A página
    exibe uma lista com todos os membros da UMADJAF cadastrados no site.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de gerenciamento de membros.
    '''

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
            'is_admin': is_admin,
            'members_all': members
        }
    )


# Função de aprovação de membro
@authenticated_user
def member_positive(request, member_id,
                    is_authenticated,
                    is_admin,
                    is_media_manager,
                    is_devotion_manager,
                    is_coordinator,
                    is_umadjaf
                    ):
    '''
    Função para aprovar um membro

    Esta view aprova um membro da UMADJAF. A view recebe o ID do membro a ser
    aprovado e altera o status do membro para aprovado.

    Parâmetros:
        - request: Requisição HTTP.
        - member_id: ID do membro a ser aprovado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Redireciona o usuário para a página anterior.
    '''

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
def member_negative(request, member_id,
                    is_authenticated,
                    is_admin,
                    is_media_manager,
                    is_devotion_manager,
                    is_coordinator,
                    is_umadjaf
                    ):
    '''
    Função para reprovar um membro

    Esta view reprova um membro da UMADJAF. A view recebe o ID do membro a ser
    reprovado e altera o status do membro para reprovado.

    Parâmetros:
        - request: Requisição HTTP.
        - member_id: ID do membro a ser reprovado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Redireciona o usuário para a página anterior.
    '''

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
