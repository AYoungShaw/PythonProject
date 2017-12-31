from django.shortcuts import render
from django.http import HttpResponse
# 重定向
from django.shortcuts import redirect
from news.models import Column, Article
# Create your views here.


def index(request):
    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)
    content = {'home_display_columns': home_display_columns,
               'nav_display_columns': nav_display_columns}
    return render(request, 'index.html', content)


def column_detail(request, column_slug):
    column = Column.objects.get(slug=column_slug)
    content = {'column': column}
    return render(request, 'news/column.html', content)


def article_detail(request, pk, article_slug):
    article = Article.objects.get(pk=pk)

    if article_slug != article.slug:
        return redirect(article, permanent=True)

    content = {'article': article}
    return render(request, 'news/article.html', content)

