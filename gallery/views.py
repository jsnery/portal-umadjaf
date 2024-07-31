from django.shortcuts import redirect, render
from utils.decorators import authenticated_user
from events.models import Event
from .models import Gallery, GalleryMarked, GalleryMarkedUser
from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.paginator import Paginator


'''
É utilizado o decorator @authenticated_user para verificar se o usuário está
autenticado.

Ele entrega os seguintes parâmetros para as views:
    - is_authenticated: Indica se o usuário está autenticado.
    - is_admin: Indica se o usuário é um administrador.
    - is_media_manager: Indica se o usuário é um gerente de mídia.
    - is_devotion_manager: Indica se o usuário é um gerente de devoções.
    - is_coordinator: Indica se o usuário é um coordenador.
    - is_umadjaf: Indica se o usuário é um membro da UMADJAF.
'''


# Adicionar foto à galeria
@authenticated_user
def add_to_gallery(request,
                   is_authenticated,
                   is_admin,
                   is_media_manager,
                   is_devotion_manager,
                   is_coordinator,
                   is_umadjaf
                   ):
    '''
    Função para adicionar foto à galeria de fotos dos eventos

    Esta função adiciona uma foto à galeria de fotos dos eventos. A função
    renderiza a página de adição de fotos à galeria.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de adição de fotos à galeria.
    '''

    notification = False

    if not is_authenticated:
        return redirect('gallery:gallery')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    all_events = Event.objects.all().order_by('-id')

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        image = request.FILES.get('image')
        author_id = request.user.id

        if not Event.objects.filter(id=event_id).exists():
            event_date = request.POST.get('event_date')
            if event_date == '':
                notification = True
                return render(
                    request,
                    'gallery/pages/add_to_gallery.html',
                    context={
                        'is_authenticated': is_authenticated,
                        'is_admin': is_admin,
                        'is_media_manager': is_media_manager,
                        'all_events': all_events,
                        'notification': notification
                    }
                )
            event_date_ = datetime.strptime(event_date, '%Y-%m-%d')
        else:
            event_date_ = Event.objects.get(id=event_id).date

        if event_id == 0 or event_id == '0':
            event_id = int(''.join([i for i in event_date if i.isdigit()]))

        gallery = Gallery(
            event_id=event_id,
            event_date=event_date_,
            image=image,
            author_id=author_id
        )
        gallery.save()

        gallery_marked = GalleryMarked(gallery=gallery)
        gallery_marked.save()

        return redirect('gallery:add_to_gallery')

    return render(
        request,
        'gallery/pages/add_to_gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'all_events': all_events,
            'notification': notification
        }
    )


# Galeria de fotos dos eventos
@authenticated_user
def gallery(request,
            is_authenticated,
            is_admin,
            is_media_manager,
            is_devotion_manager,
            is_coordinator,
            is_umadjaf):
    '''
    View para a página de galeria de fotos dos eventos

    Esta view renderiza a página de galeria de fotos dos eventos. A página
    exibe todas as fotos dos eventos cadastradas no sistema.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de galeria de fotos dos eventos.
    '''

    gallerie = Gallery.objects.all().order_by('-id')
    events = Event.objects.all().order_by('-id')
    user_id = request.user.id

    gallerie_paginator = Paginator(gallerie, 10)  # 8 artigos por página
    page_number = request.GET.get('page')  # Página atual
    page_gallerie = gallerie_paginator.get_page(page_number)
    user_id = request.user.id

    return render(
        request, 'gallery/pages/gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_umadjaf': is_umadjaf,
            'user_id': user_id,
            'galleries': page_gallerie,
            'events': events
        }
    )


# Busca de fotos por evento
@authenticated_user
def search_gallery(request,
                   is_authenticated,
                   is_admin,
                   is_media_manager,
                   is_devotion_manager,
                   is_coordinator,
                   is_umadjaf
                   ):
    '''
    Função para buscar fotos por evento na galeria

    Esta função busca fotos por evento na galeria de fotos dos eventos. A
    função renderiza a página de galeria de fotos dos eventos com as fotos
    do evento selecionado.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de galeria de fotos dos eventos com as fotos do evento selecionado.
    '''

    gallerie = Gallery.objects.all().order_by('-id')
    events = Event.objects.all().order_by('-id')
    user_id = request.user.id

    search = request.GET.get('eventSelect')
    if search:
        print("Pesquisa: ", search)
        gallerie = Gallery.objects.filter(event_id=search).order_by('-id')

        if search == '0':
            gallerie = Gallery.objects.all().order_by('-id')
            for event in events:
                gallerie = gallerie.exclude(event_id=event.id)
    else:
        redirect('gallery:gallery')

    gallerie_paginator = Paginator(gallerie, 10)  # 8 artigos por página
    page_number = request.GET.get('page')  # Página atual
    page_gallerie = gallerie_paginator.get_page(page_number)
    user_id = request.user.id

    return render(
        request, 'gallery/pages/gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_umadjaf': is_umadjaf,
            'user_id': user_id,
            'galleries': page_gallerie,
            'events': events
        }
    )


# Gerenciador de Galeria
@authenticated_user
def gallery_manager(request,
                    is_authenticated,
                    is_admin,
                    is_media_manager,
                    is_devotion_manager,
                    is_coordinator,
                    is_umadjaf
                    ):

    if not is_authenticated:
        return redirect('gallery:gallery')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    galleries = Gallery.objects.all().order_by('-id')

    return render(
        request, 'gallery/pages/manager_gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'galleries': galleries
        }
    )


@authenticated_user
def gallery_photo_delete(request, photo_id,
                         is_authenticated,
                         is_admin,
                         is_media_manager,
                         is_devotion_manager,
                         is_coordinator,
                         is_umadjaf
                         ):

    if not is_authenticated:
        return redirect('gallery:gallery')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=photo_id)
    print(gallery)
    gallery.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''
As funções abaixo são utilizadas para gerenciar as marcações de fotos na
galeria de fotos dos eventos.

Os usuários podem solicitar a marcação de fotos na galeria de fotos dos
eventos. Os gerentes de mídia e administradores podem gerenciar as marcações
de fotos na galeria de fotos dos eventos.
'''


# Solicitar marcação de foto
@authenticated_user
def mark_gallery(request, gallery_id,
                 is_authenticated,
                 is_admin,
                 is_media_manager,
                 is_devotion_manager,
                 is_coordinator,
                 is_umadjaf
                 ):
    '''
    Função para solicitar marcação de foto na galeria

    Esta função solicita a marcação de uma foto na galeria de fotos dos
    eventos. A função adiciona a solicitação de marcação ao banco de dados.

    Parâmetros:
        - request: Requisição HTTP.
        - gallery_id: ID da foto a ser marcada.
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
        return redirect('gallery:gallery')

    if not is_umadjaf:
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=gallery_id)
    gallery_marked = GalleryMarked.objects.get(gallery=gallery)
    user_id = request.user.id

    solicitation = GalleryMarkedUser(
        gallery_marked=gallery_marked,
        user_id=user_id
    )

    solicitation.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Cancelar solicitação de marcação de foto
@authenticated_user
def unmark_gallery(request, gallery_id,
                   is_authenticated,
                   is_admin,
                   is_media_manager,
                   is_devotion_manager,
                   is_coordinator,
                   is_umadjaf
                   ):
    '''
    Função para cancelar solicitação de marcação de foto na galeria

    Esta função cancela a solicitação de marcação de uma foto na galeria de
    fotos dos eventos. A função remove a solicitação de marcação do banco de
    dados.

    Parâmetros:
        - request: Requisição HTTP.
        - gallery_id: ID da foto a ser desmarcada.
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
        return redirect('gallery:gallery')

    if not is_umadjaf:
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=gallery_id)
    gallery_marked = GalleryMarked.objects.get(gallery=gallery)
    user_id = request.user.id

    solicitation = GalleryMarkedUser.objects.get(
        gallery_marked=gallery_marked,
        user_id=user_id
    )

    solicitation.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Gerenciamento de marcações de fotos
@authenticated_user
def gallery_marked_user_manager(request,
                                is_authenticated,
                                is_admin,
                                is_media_manager,
                                is_devotion_manager,
                                is_coordinator,
                                is_umadjaf
                                ):
    '''
    Função para gerenciar marcações de fotos na galeria

    Esta função gerencia as marcações de fotos na galeria de fotos dos eventos.
    A função renderiza a página de gerenciamento de marcações de fotos.

    Parâmetros:
        - request: Requisição HTTP.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - A página de gerenciamento de marcações de fotos.
    '''

    if not is_authenticated:
        return redirect('gallery:gallery')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    galleries_marked_user = GalleryMarkedUser.objects.all().order_by('-id')

    return render(
        request, 'gallery/pages/mark_manager.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'galleries_marked': galleries_marked_user,
        }
    )


# Marcação de foto confirmada
@authenticated_user
def check_mark_gallery(request, gallery_id, user_id,
                       is_authenticated,
                       is_admin,
                       is_media_manager,
                       is_devotion_manager,
                       is_coordinator,
                       is_umadjaf
                       ):
    '''
    Função para marcar foto como confirmada na galeria

    Esta função marca uma foto como confirmada na galeria de fotos dos eventos.
    A função altera o status de confirmação da marcação da foto no banco de
    dados.

    Parâmetros:
        - request: Requisição HTTP.
        - gallery_id: ID da foto a ser marcada.
        - user_id: ID do usuário que marcou a foto.
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
        return redirect('gallery:gallery')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=gallery_id)
    gallery_marked = GalleryMarked.objects.get(gallery=gallery)
    marked_user = GalleryMarkedUser.objects.get(
        gallery_marked=gallery_marked,
        user_id=user_id
        )

    if marked_user.marked_confirm:
        marked_user.marked_confirm = False
    else:
        marked_user.marked_confirm = True

    marked_user.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
