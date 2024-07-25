from django.shortcuts import render, get_object_or_404
from functools import wraps
from django.http import HttpResponseRedirect
import requests
from .models import Articles
from users.models import User, IsUmadjaf, UserRoles, Roles
from django.utils import timezone
from django.shortcuts import redirect
from django.db.models import Q

# Create your views here.

today = timezone.now()


# Decorator para verificar se o usuário está autenticado e se é um membro da equipe de mídia
def authenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated  # Verifica se o usuário está logado
        if is_authenticated:
            is_admin = request.user.is_staff # Verifica se o usuário é admin
            is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
            is_devotion_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='DevotionManager')).exists()
            is_coordinator = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='Coordinator')).exists()
            is_umadjaf = IsUmadjaf.objects.get(user_id=request.user).checked
        else:
            is_admin = False
            is_media_manager = False
            is_devotion_manager = False
            is_coordinator = False
            is_umadjaf = False

        return view_func(request, *args, **kwargs,
                         is_authenticated=is_authenticated,
                         is_admin=is_admin,
                         is_media_manager=is_media_manager,
                         is_devotion_manager=is_devotion_manager,
                         is_coordinator=is_coordinator,
                         is_umadjaf=is_umadjaf
                         )

    return wrapper


# Postar artigos
@authenticated_user
def publish_articles(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    notification = False

    if not is_authenticated:
        return redirect('articles:all_articles')

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    if request.method == 'POST':
        title = request.POST.get('title')
        book = request.POST.get('book')
        chapter = request.POST.get('chapter')
        verse = request.POST.get('verse')
        verse2 = request.POST.get('verse2')

        if verse2 == '':
            reference = f'{book} {chapter}:{verse}'
        else:
            reference = f'{book} {chapter}:{verse}-{verse2}'

        content = request.POST.get('content')
        image = request.FILES.get('banner')
        author_id = request.user.id

        if not title or not content:
            notification = True
            return render(
                request,
                'articles/create_articles.html',
                context={
                    'is_authenticated': is_authenticated,
                    'alert': notification
                }
            )

        article = Articles(
            title=title,
            versicle=reference,
            text=content,
            author_id=author_id
        )

        if image:
            article.banner = image

        if is_admin or is_coordinator or is_devotion_manager:
            article.is_official = True

        if is_umadjaf:
            article.post_unlock = True

        article.save()
        return redirect('users:profile')

    return render(
        request,
        'articles/create_articles.html',
        context={
            'is_authenticated': is_authenticated,
            'alert': alert,
        }
    )


# Ver artigo
@authenticated_user
def article(request, article_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    article = Articles.objects.get(id=article_id)
    user_id = request.user.id

    try:
        publisher = User.objects.get(id=article.author_id).complete_name
    except User.DoesNotExist:
        publisher = "Usuário não encontrado"

    publisher_id = article.author_id
    article_reference = article.versicle

    api_url = f'https://bible-api.com/{article_reference}?translation=almeida'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        verse_text = data['text']
    else:
        verse_text = "Passagem bíblica não encontrada."

    return render(
        request, 'articles/article.html',
        {
            'is_umadjaf': is_umadjaf,
            'article': article,
            'publisher': publisher,
            'publisher_id': publisher_id,
            'verse_text': verse_text,
            'is_authenticated': is_authenticated,
            'user_id': user_id,
            'is_admin': is_admin,
            'is_devotion_manager': is_devotion_manager,
            'is_coordinator': is_coordinator
        }
    )


# Todos os artigos
@authenticated_user
def all_articles(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    articles = Articles.objects.all().filter(post_unlock=True).order_by('-id')
    user_id = request.user.id

    return render(
        request, 'articles/all_articles.html',
        {
            'articles': articles,
            'is_umadjaf': is_umadjaf,
            'is_authenticated': is_authenticated,
            'user_id': user_id,
            'is_admin': is_admin
        }
    )


# Pesquisar artigos
@authenticated_user
def search_articles(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    user_id = request.user.id
    search = request.GET.get('search')

    if search:
        words = search.split()
        query = Q()
        for word in words:
            query |= Q(title__icontains=word) | Q(text__icontains=word) | Q(versicle__icontains=word)
        articles = Articles.objects.filter(query).distinct().filter(post_unlock=True).order_by('-id')
        print("Artigos encontrados: ", articles)
    else:
        articles = Articles.objects.none()
        print("Nenhum artigo encontrado")

    return render(
        request, 'articles/all_articles.html',
        {
            'articles': articles,
            'is_umadjaf': is_umadjaf,
            'is_authenticated': is_authenticated,
            'user_id': user_id,
            'is_admin': is_admin
        }
    )


# Funções de gerenciamento de Artigos
@authenticated_user
def articles_manager(request, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):
    articles = Articles.objects.all().order_by('-id')

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    return render(
        request,
        'articles/articles_manager.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_devotion_manager': is_devotion_manager,
            'is_coordinator': is_coordinator,
            'articles_all': articles
        }
    )


# Verificar artigo
@authenticated_user
def article_verify(request, article_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    article = Articles.objects.get(id=article_id)
    article.is_official = True
    article.post_unlock = True
    article.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Desverificar artigo
@authenticated_user
def article_unverify(request, article_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    article = Articles.objects.get(id=article_id)
    article.is_official = False
    article.post_unlock = False
    article.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Deletar artigo
@authenticated_user
def article_delete(request, article_id, is_authenticated=False, is_admin=False, is_media_manager=False, is_devotion_manager=False, is_coordinator=False, is_umadjaf=False):

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    article = get_object_or_404(Articles, pk=article_id)
    article.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
