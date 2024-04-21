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
        'home/pages/home.html',
        context={
            'title': 'Teste de Template Django',
            'message': 'Welcome to the home page!',
            'carousel': {
                'card1': {
                    'image': {'url': 'src/home/banners/1.png'},
                    'title': 'Membro',
                },
                'card2': {
                    'image': {'url': 'src/home/banners/2.png'},
                    'title': 'Coordenação',
                },
                'card3': {
                    'image': {'url': 'src/home/banners/3.png'},
                    'title': 'Banda',
                }
            },
            'article': {
                'card1': {
                    'image': {'url': 'articles/src/banners/1.png'},
                    'title': 'Artigo 1',
                    'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                },
                'card2': {
                    'image': {'url': 'articles/src/banners/2.png'},
                    'title': 'Artigo 2',
                    'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                },
                'card3': {
                    'image': {'url': 'articles/src/banners/3.png'},
                    'title': 'Artigo 3',
                    'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                },
                'card4': {
                    'image': {'url': 'articles/src/banners/3.png'},
                    'title': 'Artigo 4',
                    'text': 'Loren ipsum dolor sit amet, consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                }
            },
            'next_event': 'src/home/events/1.png'
        }
    )
