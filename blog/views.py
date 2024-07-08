import logging
from typing import Mapping, Any

from django.db.models.query import QuerySet
from django.db.models import Q
from django.views import generic
from django.contrib.postgres.search import SearchQuery
from django.utils.html import escape

from .models import Tag, Article

logger = logging.getLogger('django')


class IndexView(generic.ListView):
    template_name: str = "blog/index.html"
    context_object_name: str = "articles"
    
    def get_queryset(self) -> QuerySet[Article]:
        """
        Return articles according conditions.
        """

        query: str | None  = self.request.GET.get('q', None)
        tag: str | None  = self.request.GET.get('tag', None)

        conditions = None

        if query is not None and query:

            clean_query = escape(query)
            post_query = SearchQuery(clean_query)

            conditions = Q(title__search=post_query)
            ...
            
        if tag is not None and tag:

            clean_tag = escape(tag)

            if conditions is None:
                conditions = Q(tags__name__exact=clean_tag)
            else:
                conditions &= Q(tags__name__exact=clean_tag)
            ...

        if conditions is not None:
            return Article.objects.filter(conditions).order_by('-id')[:3]
        else:            
            return Article.objects.all()[:3]
    
    def get_context_data(self, *args, **kwargs) -> Mapping[str, Any]:
        """
        Return updated context with added Tags and previous query.
        """
        context = super().get_context_data(*args, **kwargs)
        
        prev_query: str | None = self.request.GET.get('q', None)
        prev_tag: str | None = self.request.GET.get('tag', None)
        
        
        context['tags'] = Tag.objects.all()
        context['prev_query'] = escape(prev_query) if prev_query is not None else prev_query
        context['prev_tag'] = escape(prev_tag) if prev_tag is not None else prev_tag
        
        return context 
    ...


class ArticlesView(generic.ListView):
    template_name: str = "blog/list.html"
    context_object_name: str = "articles"
    paginate_by: int = 2
    
    def get_queryset(self) -> QuerySet[Article]:
        """
        Return all articles.
        """

        return Article.objects.all()
    ...


class DetailView(generic.DetailView):
    model = Article
    template_name = "blog/detail.html"
    ...
