import logging
from typing import Mapping, Any

from django.db.models.query import QuerySet
from django.db.models import Q
from django.views import generic
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.utils.html import escape
from django.core.cache import cache

from .models import Tag, Article

logger = logging.getLogger('django')


class IndexView(generic.ListView):
    """
    A view that displays a list of articles based on search conditions.
    """

    template_name: str = "blog/index.html"
    context_object_name: str = "articles"
    
    def get_queryset(self) -> QuerySet[Article]:
        """
        Return articles according to the search conditions.

        Returns:
            QuerySet[Article]: The queryset of articles.
        """
        cache_key: str = 'multi'
        conditions = None

        query: str | None  = self.request.GET.get('q', None)
        tag: str | None  = self.request.GET.get('tag', None)

        if query:
            # Clean and escape the query
            clean_query = escape(query)
            cache_key = f'{cache_key}-{clean_query}'
            post_query = SearchQuery(clean_query, search_type='phrase')

            conditions = Q(search=post_query)
            
        if tag:
            # Clean and escape the tag
            clean_tag = escape(tag)
            cache_key = f'{cache_key}-{clean_tag}'

            if conditions is None:
                conditions = Q(tags__name__exact=clean_tag)
            else:
                conditions &= Q(tags__name__exact=clean_tag)

        articles: QuerySet[Article] | None = cache.get(cache_key)

        if conditions:
            if articles is None:
                articles = Article.objects.annotate(search=SearchVector('title')).filter(conditions)[:3]
                cache.set(cache_key, articles)
                
            return articles
        else:
            if articles is None:
                articles = Article.objects.all()[:3]
                cache.set(cache_key, articles)
                
            return articles
    
    def get_context_data(self, *args, **kwargs) -> Mapping[str, Any]:
        """
        Return the updated context with added tags and previous query.

        Returns:
            Mapping[str, Any]: The updated context.
        """
        context = super().get_context_data(*args, **kwargs)
        cache_key: str = 'tags'
        
        prev_query: str | None = self.request.GET.get('q', None)
        prev_tag: str | None = self.request.GET.get('tag', None)

        tags: QuerySet[Tag] | None = cache.get(cache_key)

        if tags is None:
            tags = Tag.objects.all()
            cache.set(cache_key, tags)
            
        context['tags'] = tags
        context['prev_query'] = escape(prev_query) if prev_query is not None else prev_query
        context['prev_tag'] = escape(prev_tag) if prev_tag is not None else prev_tag
        
        return context


class ArticlesView(generic.ListView):
    template_name: str = "blog/list.html"
    context_object_name: str = "articles"
    paginate_by: int = 2
    
    def get_queryset(self) -> QuerySet[Article]:
        """
        This method retrieves all articles from the database or from cache if they exist there. 

        Returns:
            QuerySet[Article]: All articles in the database.
        """
        cache_key: str = 'articles'

        articles: QuerySet[Article] | None = cache.get(cache_key)

        if articles is None:
            articles = Article.objects.all()
            cache.set(cache_key, articles)
            
        return articles


class DetailView(generic.DetailView):
    model = Article
    template_name = "blog/detail.html"
