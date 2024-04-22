# from django.http import HttpResponse
from django.shortcuts import render


article = {
            'article1': {
                'image': {'url': 'articles/src/banners/1.png'},
                'title': 'Artigo 1',
                'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
                'link': 'https://www.google.com.br'
            },
            'article2': {
                'image': {'url': 'articles/src/banners/2.png'},
                'title': 'Artigo 2',
                'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
                'link': 'https://www.google.com.br'
            },
            'article3': {
                'image': {'url': 'articles/src/banners/3.png'},
                'title': 'Artigo 3',
                'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
                'link': 'https://www.google.com.br'
            },
            'article4': {
                'image': {'url': 'articles/src/banners/3.png'},
                'title': 'Artigo 4',
                'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
                'link': 'https://www.google.com.br'
            }
}

carousel = {
            'card1': {
                'image': {'url': 'home/src/banners/1.png'},
                'title': 'Membro',
            },
            'card2': {
                'image': {'url': 'home/src/banners/2.png'},
                'title': 'Coordenação',
            },
            'card3': {
                'image': {'url': 'home/src/banners/3.png'},
                'title': 'Banda',
            }
}

next_event = {
            'bg': 'home/src/events/1.png',
            'banner': 'home/src/events/2.png',
}

page = 'UMADJAF'

title = 'Teste de Template Django'

message = 'Welcome to the home page!'

is_authenticated = True



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
        'home/pages/home.html',
        context={
            'is_authenticated': is_authenticated,
            'page': page,
            'title': title,
            'message': message,
            'carousel': carousel,
            'article': article,
            'next_event': next_event
        }
    )
