from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone
from articles.models import Articles
from events.models import Event
from users.models import IsUmadjaf, Roles, UserRoles
from .models import Carrousel


# decorator para verificar se o usuário está autenticado e se é um membro da equipe de mídia
def authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica se o usuário está logado
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            is_admin = request.user.is_staff  # Verifica se o usuário é admin
            is_media_manager = UserRoles.objects.filter(
                user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
            is_devotional_manager = UserRoles.objects.filter(
                user_id=request.user, role_id=Roles.objects.get(role='DevotionManager')).exists()
            is_coordinator = UserRoles.objects.filter(
                user_id=request.user, role_id=Roles.objects.get(role='Coordinator')).exists()
            if IsUmadjaf.objects.filter(user_id=request.user).exists():
                is_umadjaf = IsUmadjaf.objects.get(
                    user_id=request.user).checked
        else:
            is_admin = False
            is_media_manager = False
            is_devotional_manager = False
            is_coordinator = False
            is_umadjaf = False

        return view_func(request, *args, **kwargs,
                         is_authenticated=is_authenticated,
                         is_admin=is_admin,
                         is_media_manager=is_media_manager,
                         is_devotional_manager=is_devotional_manager,
                         is_coordinator=is_coordinator,
                         is_umadjaf=is_umadjaf
                         )

    return wrapper


# Página inicial
@authenticated_user
def home(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotional_manager=False, is_coordinator=False, is_umadjaf=False):
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
def carrousel(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotional_manager=False, is_coordinator=False, is_umadjaf=False):
    carrousel_itens = Carrousel.objects.all().order_by('-id')

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
def carrousel_add(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotional_manager=False, is_coordinator=False, is_umadjaf=False):

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
def carrousel_delete(request, item_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotional_manager=False, is_coordinator=False, is_umadjaf=False):

    if not is_authenticated:
        return redirect('home')

    if not (is_media_manager or is_admin):
        return redirect('home')

    carrousel = Carrousel.objects.get(id=item_id)
    carrousel.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
