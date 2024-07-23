from django.http import HttpResponse
from django.shortcuts import render, redirect
from events.models import Event
from articles.models import Articles
from .models import Carrousel
from users.models import IsUmadjaf
from django.utils import timezone


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

next_event = {
            'bg': 'home/src/events/1.png',
            'banner': 'home/src/events/2.png',
}

page = 'UMADJAF'

title = 'Teste de Template Django'

message = 'Welcome to the home page!'


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
    
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin

    evento = Event.objects.filter(is_general=True, date__gte=timezone.now()).order_by('date').first()
    articles = Articles.objects.filter(is_official=True).filter(post_unlock=True).order_by('-id')[:3]
    carousel = Carrousel.objects.filter(active=True).order_by('-id')

    is_umadjaf = False
    if request.user.is_authenticated:
        user_id = request.user.id
        member_ok = IsUmadjaf.objects.filter(user_id=user_id).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=user_id).checked

    return render(
        request,
        'home/pages/home.html',
        context={
            'is_authenticated': request.user.is_authenticated,
            'is_umadjaf': is_umadjaf,
            'is_admin': user_is_admin,
            'page': page,
            'title': title,
            'message': message,
            'carousel': carousel,
            'article': articles,
            'next_event': evento
        }
    )


def carrousel(request):
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin
    carrousel_itens = Carrousel.objects.all().order_by('-id')

    if request.method == 'POST':
        print("Iniciando a atualização dos itens do carrossel...")
        form_data = dict(request.POST.items())
        print(form_data)
        for item, status in form_data.items():
            if item == 'csrfmiddlewaretoken':
                print("Ignorando token CSRF.")
                continue
            if item.startswith('itemid_'):
                item_id = int(item.split('_')[1])
                print(f"Item ID: {type(item_id)}")
                carrousel_item = Carrousel.objects.get(id=item_id)
                carrousel_item.active = (status == 'on')
                carrousel_item.save()
                print(f"Item ID {item_id} atualizado para {'ativo' if status == 'on' else 'inativo'}.")
        print("Atualização dos itens do carrossel concluída.")

        return redirect('home')

    return render(
        request,
        'carrousel/pages/carrousels.html',
        context={
            'is_authenticated': request.user.is_authenticated,
            'is_admin': user_is_admin,
            'carrousel': carrousel_itens,
        }
    )


def carrousel_editor(request):
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
    is_authenticated = request.user.is_authenticated
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin

    if not is_authenticated:
        redirect('home')

    if not user_is_admin:
        redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        carrousel = Carrousel(
            title=title,
            description=description,
            image=image,
            author_id=request.user.id
        )

        carrousel.save()

        return redirect('carrousel')

    return render(
        request,
        'carrousel/pages/carrousel_editor.html',
        context={
            'is_authenticated': request.user.is_authenticated,
            'is_admin': user_is_admin,
        }
    )


def carrousel_delete(request, item_id):
    is_authenticated = request.user.is_authenticated
    user_is_admin = request.user.is_staff # Verifica se o usuário é admin

    if not is_authenticated:
        redirect('home')

    if not user_is_admin:
        redirect('home')

    carrousel = Carrousel.objects.get(id=item_id)
    carrousel.delete()

    return redirect('carrousel')
