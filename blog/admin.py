from django.contrib import admin
from .models import Article,SavedArticle,Tags



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')

    class Media:
        js = [
            '//cdn.ckeditor.com/4.14.0/standard/ckeditor.js',
    ]

@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Tags)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('id','text')

