from django import forms  # type: ignore
from profiles.models import UserRoles, IsUmadjaf, Roles, User


class UserForm(forms.ModelForm):
    is_umadjaf = forms.BooleanField(label='Aguardando:', required=False)

    class Meta:
        model = User
        fields = ['is_umadjaf', 'is_staff', 'is_superuser']  # Adicione aqui os campos que você deseja editar


class UserRolesForm(forms.ModelForm):
    role_id = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        empty_label='Selecione um cargo',
        label='Permissão'
    )

    class Meta:
        model = UserRoles
        fields = ['role_id']  # Adicione aqui os campos que você deseja editar


class IsUmadjafForm(forms.ModelForm):
    checked = forms.BooleanField(label='Umadjaf:', required=False)

    class Meta:
        model = IsUmadjaf
        fields = ['checked']  # Adicione aqui os campos que você deseja editar