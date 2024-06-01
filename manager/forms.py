from django import forms  # type: ignore
from profiles.models import UserRoles, IsUmadjaf, Roles, User
from .models import Congregations


# Formulários do novo painel de controle


# Formulário de edição de usuário
class UserForm(forms.ModelForm):
    complete_name = forms.CharField(label='Nome Completo', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    number_phone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    church = forms.ModelChoiceField(
        queryset=Congregations.objects.all(),
        empty_label='Selecione uma igreja',
        label='Congregação'
    )

    class Meta:
        model = User
        fields = ['complete_name', 'number_phone', 'church']  # Adicione aqui os campos que você deseja editar

    def save(self, commit=True):
        instance = super().save(commit=False)
        print((self.cleaned_data['church'].id))
        print(instance)
        instance.church = int(self.cleaned_data['church'].id)
        if commit:
            instance.save()
        return instance


class UserRolesForm(forms.ModelForm):
    role_id = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        empty_label='Selecione um cargo',
        label='Permissão'
    )

    class Meta:
        model = UserRoles
        fields = ['role_id']  # Adicione aqui os campos que você deseja editar

    def save(self, commit=True):
        instance = super().save(commit=False)
        user = User.objects.get(id=instance.user_id.id)

        if str(instance.role_id) == 'Admin':  # Substitua 'name' pelo campo que contém o nome do cargo
            user.is_staff = True
            user.is_superuser = True

            if commit:
                user.save()
        else:
            user.is_staff = False
            user.is_superuser = False

            if commit:
                user.save()
        if commit:
            instance.save()
        return instance


class IsUmadjafForm(forms.ModelForm):
    checked = forms.BooleanField(label='Umadjaf:', required=False)

    class Meta:
        model = IsUmadjaf
        fields = ['checked']  # Adicione aqui os campos que você deseja editar


# Formulário de adição de congregação
class CongregationForm(forms.ModelForm):
    name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    address = forms.CharField(label='Endereço', widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = Congregations
        fields = ['name', 'address']  # Adicione aqui os campos que você deseja editar