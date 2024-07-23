from django.shortcuts import render, redirect
from django.utils import timezone
from users.models import IsUmadjaf, UserRoles, Roles
from manager.models import Congregations
from .models import Event


def eventos(request):
    events = Event.objects.filter(date__gte=timezone.now())

    is_umadjaf = False
    if request.user.is_authenticated:
        user_id = request.user.id
        member_ok = IsUmadjaf.objects.filter(user_id=user_id).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=user_id).checked

    return render(
        request,
        'events/pages/events.html',
        context={
            'events': events,
            'is_authenticated': request.user.is_authenticated,
            'is_umadjaf': is_umadjaf,
        }
    )


def criar_evento(request):
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
    is_admin = request.user.is_staff # Verifica se o usuário é admin
    is_cordinator = UserRoles.objects.filter(user_id=request.user.id, role_id=Roles.objects.get(role='Coordinator')).exists()

    if not is_authenticated:
        return redirect('events:eventos')
    elif not is_cordinator:
        if is_admin:
            pass
        else:
            return redirect('events:eventos')

    is_umadjaf = False
    if request.user.is_authenticated:
        user_id = request.user.id
        member_ok = IsUmadjaf.objects.filter(user_id=user_id).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=user_id).checked

    congregations = Congregations.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        theme = request.POST.get('theme')
        date = request.POST.get('date')
        hour = request.POST.get('hour')
        congregation_id = request.POST.get('congregation_id')
        logo = request.FILES.get('logo')
        background = request.FILES.get('background')

        # if not title or not content:
        #     messages.error(request, 'Título e conteúdo são obrigatórios.')
        #     return render(request, 'articles/create_articles.html')

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

        if is_cordinator:
            event.is_general = False

        if is_admin:
            event.is_general = True

        event.save()
        return redirect('events:eventos')  # Substitua 'alguma_url_para_listar_artigos' pela URL de destino

    return render(
        request,
        'events/pages/create_event.html',
        context={
            'congregations': congregations,
            'is_authenticated': is_authenticated,
            'is_umadjaf': is_umadjaf,
        }
    )