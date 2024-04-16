# from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    '''
    O render() é uma função que renderiza o template 
    especificado e retorna o objeto HttpResponse com
    o conteúdo do template.

    O primeiro argumento é o objeto request, que é
    obrigatório. O segundo argumento é o caminho do template
    que será renderizado. O terceiro argumento é um
    dicionário opcional que contém variáveis que serão
    passadas para o template.
    '''
    return render(
        request,
        'home/home.html',
        context={
            'title': 'Teste de Template Django',
            'message': 'Welcome to the home page!'
        }
    )


def news(request):
    return render(request, 'home/news.html')
