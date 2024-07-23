from django import forms  # type: ignore
from users.models import IsUmadjaf, Roles, User, UserRoles
from .models import Congregations
from events.models import Event


# Formulários do novo painel de controle


# Formulário de edição de usuário
class UserForm(forms.ModelForm):
    complete_name = forms.CharField(
        label='Nome Completo', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    number_phone = forms.CharField(
        label='Telefone', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    church = forms.ModelChoiceField(
        queryset=Congregations.objects.all(),
        empty_label='Selecione uma igreja',
        label='Congregação'
    )

    class Meta:
        model = User
        # Adicione aqui os campos que você deseja editar
        fields = ['complete_name', 'number_phone', 'church']

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
            user.is_superuser = False

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
    name = forms.CharField(label='Nome', widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))
    address = forms.CharField(
        label='Endereço', widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = Congregations
        # Adicione aqui os campos que você deseja editar
        fields = ['name', 'address']


# Formulário de calendário
class CalendarForm(forms.ModelForm):
    title = forms.CharField(
        label='Título', 
        widget=forms.TextInput(attrs={
            'autocomplete': 'off', 
            'id': 'title-calendar', 
            'class': 'form-control'  # Adiciona a classe do Bootstrap
        })
    )
    date = forms.DateField(
        label='Data', 
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'  # Adiciona a classe do Bootstrap
        })
    )
    theme = forms.CharField(
        label='Tema', 
        widget=forms.TextInput(attrs={
            'autocomplete': 'off', 
            'id': 'theme-calendar', 
            'class': 'form-control'  # Adiciona a classe do Bootstrap
        })
    )
    is_general = forms.BooleanField(
        label='Geral', 
        required=False
    )
    congregation = forms.ModelChoiceField(
        queryset=Congregations.objects.all(),
        empty_label='Selecione uma igreja',
        label='Congregação',
        widget=forms.Select(attrs={
            'class': 'form-select'  # Adiciona a classe do Bootstrap para selects
        })
    )
    logo = forms.ImageField(
        label='Logo', 
        widget=forms.FileInput(attrs={
            'class': 'form-control'  # Adiciona a classe do Bootstrap para inputs de arquivo
        })
    )
    background = forms.ImageField(
        label='Background', 
        widget=forms.FileInput(attrs={
            'class': 'form-control'  # Adiciona a classe do Bootstrap para inputs de arquivo
        })
    )

    class Meta:
        model = Event
        # Adicione aqui os campos que você deseja editar
        fields = ['title', 'date',
                  'theme', 'is_general', 'congregation', 'logo', 'background']

    title = forms.CharField(label='Título', widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'id': 'title-article'}))
    text = forms.CharField(label='Texto', widget=forms.Textarea(
        attrs={'autocomplete': 'off', 'id': 'text-article'}))
    date = forms.DateField(label='Data', widget=forms.DateInput(
        attrs={'type': 'date'}))
    banner = forms.ImageField(label='Banner')
    author_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    is_official = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Event
        # Adicione aqui os campos que você deseja editar
        fields = ['title', 'text', 'date', 'banner', 'author_id', 'is_official']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['author_id'].initial = self.user.id