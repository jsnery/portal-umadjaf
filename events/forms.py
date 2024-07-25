from django import forms  # type: ignore
from manager.models import Congregations
from .models import Event


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
