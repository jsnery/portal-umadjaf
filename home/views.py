from utils.decorators import authenticated_user
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from articles.models import Articles
from events.models import Event
from .models import Carrousel


# Página inicial
@authenticated_user
def home(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Página inicial

    Esta view renderiza a página inicial do site. A página inicial contém
    informações sobre o próximo evento, devocionais verificados e banners
    do carrossel.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página inicial do site.'''

    evento = Event.objects.filter(
        is_general=True, date__gte=timezone.now()).order_by('date').first()
    articles = Articles.objects.filter(is_official=True).filter(
        post_unlock=True).order_by('-id')[:3]
    carousel = Carrousel.objects.filter(active=True).order_by('-id')

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


# Gerir banners do carrossel
@authenticated_user
def carrousel(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Gerir banners do carrossel

    Esta view renderiza a página de gerenciamento dos banners do carrossel.
    A página exibe todos os banners do carrossel e permite que o usuário
    ative ou desative cada um deles.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de gerenciamento dos banners do carrossel.'''

    if not is_authenticated:
        return redirect('home')

    if not (is_media_manager or is_admin):
        return redirect('home')

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
                print(f"Item ID {item_id} atualizado para {
                      'ativo' if status == 'on' else 'inativo'}.")
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


# Adicionar banner do carrossel
@authenticated_user
def carrousel_add(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Adicionar banner do carrossel

    Esta view renderiza a página de adição de um novo banner do carrossel.
    A página exibe um formulário para o usuário preencher com as informações
    do novo banner.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de adição de um novo banner do carrossel.
    '''

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


# Deletar banner do carrossel
@authenticated_user
def carrousel_delete(request, item_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Deletar banner do carrossel

    Esta view deleta um banner do carrossel a partir do ID do item.

    Parâmetros:
        - request: Requisição HTTP.
        - item_id: ID do item do carrossel.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Redireciona para a página anterior.
    '''

    if not is_authenticated:
        return redirect('home')

    if not (is_media_manager or is_admin):
        return redirect('home')

    carrousel = Carrousel.objects.get(id=item_id)
    carrousel.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
