from django.shortcuts import render, get_object_or_404
from utils.decorators import authenticated_user
from django.http import HttpResponseRedirect
from .models import Articles
from users.models import User
from django.utils import timezone
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator


today = timezone.now()


# Postar devicional
@authenticated_user
def publish_articles(request,
                     is_authenticated,
                     is_admin,
                     is_media_manager,
                     is_devotion_manager,
                     is_coordinator,
                     is_umadjaf
                     ):
    '''
    Função para publicar devocionais

    Esta função permite que um usuário autenticado publique um devicional no
    sistema. O usuário deve fornecer um título, uma referência bíblica,
    o conteúdo do devicional e, opcionalmente, uma imagem de capa para o
    devicional.

    O devicional é salvo no banco de dados utilizando o modelo Articles, e é
    marcado como oficial caso o usuário seja um administrador, coordenador
    ou gerente de devoções. Caso o usuário seja um membro da UMADJAF, o
    devicional é marcado como desbloqueado.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP redirecionando o usuário para a página de perfil.
    '''

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
            'is_admin': is_admin,
            'alert': notification,
        }
    )


# Ver devicional
@authenticated_user
def article(request, article_id,
            is_authenticated,
            is_admin,
            is_media_manager,
            is_devotion_manager,
            is_coordinator,
            is_umadjaf
            ):
    '''
    Função para exibir um devicional específico

    Esta função retorna a página de um devicional específico, identificado pelo
    parâmetro 'article_id'. O devicional é obtido a partir do banco de dados,
    utilizando o modelo Articles, e é exibido na página juntamente com o
    nome do autor, a passagem bíblica referenciada e o texto da passagem.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - article_id: O ID do artigo a ser exibido.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP contendo a página do devicional específico.
        '''

    article = Articles.objects.get(id=article_id)
    user_id = request.user.id

    try:
        publisher = User.objects.get(id=article.author_id).complete_name
    except User.DoesNotExist:
        publisher = "Usuário não encontrado"

    publisher_id = article.author_id

    return render(
        request, 'articles/article.html',
        {
            'is_umadjaf': is_umadjaf,
            'article': article,
            'publisher': publisher,
            'publisher_id': publisher_id,
            'is_authenticated': is_authenticated,
            'user_id': user_id,
            'is_admin': is_admin,
            'is_devotion_manager': is_devotion_manager,
            'is_coordinator': is_coordinator
        }
    )


# Todos os devocionais
@authenticated_user
def all_articles(request,
                 is_authenticated,
                 is_admin,
                 is_media_manager,
                 is_devotion_manager,
                 is_coordinator,
                 is_umadjaf
                 ):
    '''
    Função para exibir todos os devocionais

    Esta função retorna uma lista de todos os devocionais cadastrados no
    sistema. Os devocionais são filtrados para exibir apenas aqueles que
    possuem a propriedade 'post_unlock' como True, e são ordenados em ordem
    decrescente pelo campo 'id'.

    A lista de devocionais é paginada, exibindo 8 devocionais por página.
    O usuário pode navegar entre as páginas utilizando os botões de paginação
    exibidos na página.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP contendo a página de todos os devocionais
          liberados.
    '''

    articles = Articles.objects.all().filter(post_unlock=True).order_by('-id')
    articles_paginator = Paginator(articles, 9)  # 8 artigos por página
    page_number = request.GET.get('page')  # Página atual
    page_articles = articles_paginator.get_page(page_number)
    user_id = request.user.id

    return render(
        request, 'articles/all_articles.html',
        {
            'articles': page_articles,
            'is_umadjaf': is_umadjaf,
            'is_authenticated': is_authenticated,
            'user_id': user_id,
            'is_admin': is_admin
        }
    )


# Pesquisar devicional
@authenticated_user
def search_articles(request,
                    is_authenticated,
                    is_admin,
                    is_media_manager,
                    is_devotion_manager,
                    is_coordinator,
                    is_umadjaf
                    ):
    '''
    Função para pesquisar devocionais

    Esta função realiza a pesquisa de devocionais com base em um termo de
    busca fornecido pelo usuário. O termo de busca é obtido a partir do
    parâmetro GET 'search' da requisição.

    A pesquisa é realizada utilizando o sistema de pesquisa Q() do Django,
    que permite realizar consultas complexas utilizando operadores lógicos
    como OR e AND. Neste caso, a função realiza a busca nos campos 'title',
    'text' e 'versicle' do modelo Articles, buscando por qualquer palavra
    que corresponda a algum desses campos.

    Os devocionais encontrados são filtrados para exibir apenas aqueles que
    possuem a propriedade 'post_unlock' como True, e são ordenados em ordem
    decrescente pelo campo 'id'.

    Caso nenhum termo de busca seja fornecido, a função retorna uma lista
    vazia de devocionais.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP contendo a página de resultados da pesquisa de devocionais.
    '''

    user_id = request.user.id
    search = request.GET.get('search')

    if search:
        words = search.split()
        query = Q()
        for word in words:
            query |= Q(title__icontains=word) | Q(text__icontains=word) | Q(versicle__icontains=word)
        articles = Articles.objects.filter(query).distinct().filter(post_unlock=True).order_by('-id')
        # print("Artigos encontrados: ", articles)
    else:
        articles = Articles.objects.none()
        # print("Nenhum artigo encontrado")

    articles_paginator = Paginator(articles, 9)  # 8 artigos por página
    page_number = request.GET.get('page')  # Página atual
    page_articles = articles_paginator.get_page(page_number)
    user_id = request.user.id

    return render(
        request, 'articles/all_articles.html',
        {
            'articles': page_articles,
            'is_umadjaf': is_umadjaf,
            'is_authenticated': is_authenticated,
            'user_id': user_id,
            'is_admin': is_admin
        }
    )


# Funções de gerenciamento de devocionais
@authenticated_user
def articles_manager(request,
                     is_authenticated,
                     is_admin,
                     is_media_manager,
                     is_devotion_manager,
                     is_coordinator,
                     is_umadjaf
                     ):
    '''
    Função para gerenciar devocionais

    Esta função permite que um usuário autenticado e autorizado gerencie os
    artigos cadastrados no sistema. O usuário deve ser um administrador,
    coordenador ou gerente de devoções para acessar esta página.

    Os artigos são obtidos a partir do banco de dados, utilizando o modelo
    Articles, e são exibidos na página juntamente com as seguintes informações:
    - Título do devocional
    - Nome do autor
    - Data de publicação
    - Estado do devocional (verificado ou não verificado)
    - Estado de bloqueio do devocional (bloqueado ou desbloqueado)

    Parâmetros:
        - request: A requisição HTTP recebida.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP contendo a página de gerenciamento de devocionais.
    '''
    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    articles = Articles.objects.all().order_by('-id')

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


# Verificar devicional
@authenticated_user
def article_verify(request, article_id,
                   is_authenticated,
                   is_admin,
                   is_media_manager,
                   is_devotion_manager,
                   is_coordinator,
                   is_umadjaf
                   ):
    '''
    Função para verificar devocionais

    Esta função permite que um usuário autenticado e autorizado verifique um
    devocional no sistema. O usuário deve ser um administrador, coordenador
    ou gerente de devoções para acessar esta página.

    O devocional é obtido a partir do banco de dados, utilizando o modelo
    Articles, e é marcado como oficial e desbloqueado.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - article_id: O ID do devocional a ser verificado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP redirecionando o usuário para a página anterior.
    '''


    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    article = Articles.objects.get(id=article_id)
    article.is_official = True
    article.post_unlock = True
    article.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Desverificar devicional
@authenticated_user
def article_unverify(request, article_id,
                     is_authenticated,
                     is_admin,
                     is_media_manager,
                     is_devotion_manager,
                     is_coordinator,
                     is_umadjaf
                     ):
    '''
    Função para desverificar devocionais

    Esta função permite que um usuário autenticado e autorizado desverifique um
    devocional no sistema. O usuário deve ser um administrador, coordenador
    ou gerente de devoções para acessar esta página.

    O devocional é obtido a partir do banco de dados, utilizando o modelo
    Articles, e é marcado como não oficial e bloqueado.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - article_id: O ID do devocional a ser desverificado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP redirecionando o usuário para a página anterior.
    '''

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    article = Articles.objects.get(id=article_id)
    article.is_official = False
    article.post_unlock = False
    article.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Deletar devicional
@authenticated_user
def article_delete(request, article_id,
                   is_authenticated,
                   is_admin,
                   is_media_manager,
                   is_devotion_manager,
                   is_coordinator,
                   is_umadjaf
                   ):
    '''
    Função para deletar devocionais

    Esta função permite que um usuário autenticado e autorizado delete um
    devocional no sistema. O usuário deve ser um administrador, coordenador
    ou gerente de devoções para acessar esta página.

    O devocional é obtido a partir do banco de dados, utilizando o modelo
    Articles, e é deletado do banco de dados.

    Parâmetros:
        - request: A requisição HTTP recebida.
        - article_id: O ID do devocional a ser deletado.
        - is_authenticated: Indica se o usuário está autenticado.
        - is_admin: Indica se o usuário é um administrador.
        - is_media_manager: Indica se o usuário é um gerente de mídia.
        - is_devotion_manager: Indica se o usuário é um gerente de devoções.
        - is_coordinator: Indica se o usuário é um coordenador.
        - is_umadjaf: Indica se o usuário é um membro da UMADJAF.

    Retorna:
        - Uma resposta HTTP redirecionando o usuário para a página anterior.
    '''

    if not (is_devotion_manager or is_admin or is_coordinator):
        return redirect('articles:all_articles')

    article = get_object_or_404(Articles, pk=article_id)
    article.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
