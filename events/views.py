from django.shortcuts import render, redirect
from django.utils import timezone
from users.models import IsUmadjaf, UserRoles, Roles
from manager.models import Congregations
from .models import Event


def eventos(request):
    is_authenticated = request.user.is_authenticated
    events = Event.objects.filter(date__gte=timezone.now())
    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
        is_corrdinator = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='Coordinator')).exists()
    else:
        is_admin = False
        is_media_manager = False
        is_corrdinator = False

    return render(
        request,
        'events/pages/events.html',
        context={
            'events': events,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_authenticated': is_authenticated,
            'is_cordinator': is_corrdinator
        }
    )


def criar_evento(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
        is_coordinator = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='Coordinator')).exists()
    else:
        is_admin = False
        is_media_manager = False
        is_coordinator = False

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