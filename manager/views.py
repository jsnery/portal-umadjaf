from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from profiles.models import User, UserRoles, Roles, IsUmadjaf
from .forms import UserRolesForm, IsUmadjafForm, UserForm

# Create your views here.


def users(request):
    users = User.objects.all()
    roles = Roles.objects.all()
    return render(
        request,
        'manager/pages/users.html',
        context={
            'users_all': users,
            'roles': roles
        }
    )


def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return HttpResponseRedirect(reverse('manager:users'))


def user_edit(request, user_id):
    user = User.objects.get(id=user_id)
    user_roles = UserRoles.objects.get(user_id=user_id)
    umadjaf = IsUmadjaf.objects.get(user_id=user_id)

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
        'manager/pages/partials/user_edit.html',
        context={
            'user_form': user_form,
            'user_roles_form': user_roles_form,
            'umadjaf_form': umadjaf_form
        }
    )


def users_roles(request):
    users_roles_all = UserRoles.objects.all()
    return render(
        request,
        'manager/pages/users_roles.html',
        context={
            'users_roles_all': users_roles_all
        }
    )