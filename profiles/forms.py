from django import forms  # type: ignore
from django.contrib.auth.hashers import check_password, make_password
from profiles.models import User, UserProfiles


class NoColonFileInput(forms.FileInput):
    def label_tag(self, contents, attrs=None, label_suffix=None):
        return super().label_tag(contents, attrs, label_suffix='')


class ProfileUsePictureForm(forms.ModelForm):
    profile_picture = forms.FileField(label='Alterar', widget=NoColonFileInput(
        attrs={'class': 'custom-file-input', 'id': 'form_profile_picture'}))

    class Meta:
        model = UserProfiles
        fields = ['profile_picture']


class ProfileUserForm(forms.ModelForm):
    number_phone = forms.CharField(
        label='Telefone', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    complete_name = forms.CharField(
        label='Nome Completo', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    church = forms.CharField(
        label='Igreja', widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ['number_phone', 'complete_name',
                  'church']

    def __init__(self, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['id'] = 'form_' + field


class ProfileUserPassForm(forms.ModelForm):
    current_password = forms.CharField(
        label='Senha Atual', required=False, widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    new_password = forms.CharField(
        label='Nova Senha', required=False, widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ['current_password', 'new_password']

    def __init__(self, *args, **kwargs):
        super(ProfileUserPassForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['id'] = 'form_' + field

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        if current_password and not check_password(current_password, self.instance.password):
            self.add_error('current_password',
                        "Senha atual incorreta. Por favor, tente novamente.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.password = make_password(new_password)

        if commit:
            user.save()
        return user


class ProfileUserBioForm(forms.ModelForm):
    bio = forms.CharField(
        label='Bio',
        required=False,
        max_length=75,  # Limita o campo bio a 75 caracteres
        widget=forms.Textarea(attrs={'autocomplete': 'off'}))

    class Meta:
        model = UserProfiles
        fields = ['bio']  # Adicione aqui os campos que você deseja editar

    def __init__(self, *args, **kwargs):
        super(ProfileUserBioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['id'] = 'form_' + field
