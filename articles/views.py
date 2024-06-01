from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Article

# Create your views here.


# Postar artigos
def publish_articles(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        author = request.user
        article = Article(title=title, content=content,
                          image=image, author=author)
        article.save()

    return render(request, 'articles/articles.html')


# Gerenciar artigos
def manage_articles(request):
    posts = Article.objects.all()
    return render(
        request,
        'articles/posts/all_posts.html',
        context={
            'posts': posts
        }
    )


# Deletar artigo
def delete_article(request, id):
    article = Article.objects.get(id=id)
    if article.image:
        article.image.delete(save=False)
    article.delete()
    return HttpResponseRedirect(reverse('articles:manager'))