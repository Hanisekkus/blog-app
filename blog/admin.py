from typing import Sequence

from django.contrib import admin

from .models import Tag, Article


class TagsInline(admin.TabularInline):
    model: Tag = Article.tags.through
    extra: int = 3
    ...


class ArticleAdmin(admin.ModelAdmin):
    list_display: Sequence = ["title", "content"]
    search_fields: Sequence = ["title"]
    fieldsets: Sequence[Sequence] = [
        ("Article Information", {
           "fields": ["title", "content"] 
        }),
        ("Article picture", {
           "fields": ["image"]
        })
    ]
    
    inlines: Sequence = [TagsInline] 
    ...


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
