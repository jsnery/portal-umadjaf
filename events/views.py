from django.shortcuts import render, redirect
from utils.decorators import authenticated_user
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import CalendarForm
from manager.models import Congregations
from .models import Event


# Eventos do calendário
@authenticated_user
def eventos(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Exibe os eventos futuros no portal UMADJAF.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com a lista de eventos futuros.

    Observação:
        - A função filtra os eventos com base na data atual. Apenas os eventos com data maior ou igual à data atual serão exibidos.
    '''

    events = Event.objects.filter(date__gte=timezone.now())

    return render(
        request,
        'events/pages/events.html',
        context={
            'events': events,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_authenticated': is_authenticated,
            'is_cordinator': is_coordinator
        }
    )


# Criar evento
@authenticated_user
def criar_evento(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Função para criar um novo evento no portal UMADJAF.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com o formulário de criação de evento.

    Observação:
        - A função verifica se o usuário está autenticado e se é um membro da
        equipe de mídia. Caso o usuário não esteja autenticado ou não seja um
        membro da equipe de mídia, ele será redirecionado para a página de
        eventos.
    '''

    if not is_authenticated:
        return redirect('events:eventos')

    if not (is_media_manager or is_admin or is_coordinator):
        return redirect('events:eventos')

    congregations = Congregations.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        theme = request.POST.get('theme')
        date = request.POST.get('date')
        hour = request.POST.get('hour')
        congregation_id = request.POST.get('congregation_id')
        logo = request.FILES.get('logo')
        background = request.FILES.get('background')

        event = Event(
            title=title,
            theme=theme,
            date=date,
            hours=hour,
            author_id=request.user.id,
            congregation=Congregations.objects.get(id=congregation_id)
        )

        if logo and background:
            event.logo = logo
            event.background = background

        if is_coordinator:
            event.is_general = False

        if is_media_manager or is_admin:
            event.is_general = True

        event.save()
        return redirect('events:eventos')  # Substitua 'alguma_url_para_listar_artigos' pela URL de destino

    return render(
        request,
        'events/pages/create_event.html',
        context={
            'congregations': congregations,
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_coordinator': is_coordinator
        }
    )


# Gerenciar eventos
@authenticated_user
def eventos_manager(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Função para gerenciar os eventos do portal UMADJAF.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com a lista de eventos do portal UMADJAF.

    Observação:
        - A função verifica se o usuário está autenticado e se é um membro da
        equipe de mídia. Caso o usuário não esteja autenticado ou não seja um
        membro da equipe de mídia, ele será redirecionado para a página de
        eventos.
    '''

    if not is_authenticated:
        return redirect('events:eventos')

    if not (is_media_manager or is_admin):
        return redirect('events:eventos')

    calendar = Event.objects.all()

    return render(
        request,
        'events/pages/eventos_manager.html',
        context={
            'is_authenticated': is_authenticated,
            'calendar_all': calendar
        }
    )


# Editar evento
@authenticated_user
def eventos_edit(request, calendar_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Função para editar um evento no portal UMADJAF.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponse contendo a página HTML renderizada com o formulário de edição de evento.

    Observação:
        - A função verifica se o usuário está autenticado e se é um membro da
        equipe de mídia. Caso o usuário não esteja autenticado ou não seja um
        membro da equipe de mídia, ele será redirecionado para a página de
        eventos.
    '''

    if not is_authenticated:
        return redirect('events:eventos')

    if not (is_media_manager or is_admin):
        return redirect('events:eventos')
    try:
        calendar = Event.objects.get(id=calendar_id)
    except Event.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    event_logo = calendar.logo
    event_background = calendar.background
    if request.method == 'POST':
        calendar_edit_form = CalendarForm(request.POST, request.FILES, instance=calendar)
        if calendar_edit_form.is_valid():
            # O objeto 'calendar' será atualizado com os dados do formulário
            calendar_edit_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        calendar_edit_form = CalendarForm(instance=calendar)

    return render(
        request,
        'events/pages/partials/eventos_edit.html',
        context={
            'calendar_edit_form': calendar_edit_form,
            'calendar_id': calendar_id,
            'event_logo': event_logo,
            'event_background': event_background
        }
    )


# Deletar evento
@authenticated_user
def eventos_delete(request, calendar_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    '''
    Função para deletar um evento no portal UMADJAF.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Um objeto HttpResponseRedirect redirecionando para a página de eventos.

    Observação:
        - A função verifica se o usuário está autenticado e se é um membro da
        equipe de mídia. Caso o usuário não esteja autenticado ou não seja um
        membro da equipe de mídia, ele será redirecionado para a página de
        eventos.
    '''

    if not is_authenticated:
        return redirect('events:eventos')

    if not (is_media_manager or is_admin):
        return redirect('events:eventos')

    try:
        calendar = Event.objects.get(id=calendar_id)
    except Event.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    calendar.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
