from django.http import HttpResponse
from django.shortcuts import render, redirect
from events.models import Event
from articles.models import Articles
from .models import Carrousel
from users.models import User, UserProfiles, UserRoles, Roles, IsUmadjaf
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
    is_authenticated = request.user.is_authenticated
    evento = Event.objects.filter(is_general=True, date__gte=timezone.now()).order_by('date').first()
    articles = Articles.objects.filter(is_official=True).filter(post_unlock=True).order_by('-id')[:3]
    carousel = Carrousel.objects.filter(active=True).order_by('-id')

    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()

    else:
        is_admin = False
        is_media_manager = False

    return render(
        request,
        'home/pages/home.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'carousel': carousel,
            'article': articles,
            'next_event': evento
        }
    )


def carrousel(request):
    is_authenticated = request.user.is_authenticated
    carrousel_itens = Carrousel.objects.all().order_by('-id')
    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
    else:
        is_admin = False
        is_media_manager = False

    if not is_authenticated:
        return redirect('home')

    if not (is_media_manager or is_admin):
        return redirect('home')

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
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'carrousel': carrousel_itens,
        }
    )


def carrousel_editor(request):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
    else:
        is_admin = False
        is_media_manager = False

    if not is_authenticated:
        return redirect('home')

    if not (is_media_manager or is_admin):
        return redirect('home')

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
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager
        }
    )


def carrousel_delete(request, item_id):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
    else:
        is_admin = False
        is_media_manager = False

    if not is_authenticated:
        return redirect('home')

    if not (is_media_manager or is_admin):
        return redirect('home')

    carrousel = Carrousel.objects.get(id=item_id)
    carrousel.delete()

    return redirect('carrousel')
