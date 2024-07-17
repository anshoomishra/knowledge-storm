from django.contrib import admin
from .models import Article,SavedArticle,Tags,Comment



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')



@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Tags)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('id','text')

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('id','text')