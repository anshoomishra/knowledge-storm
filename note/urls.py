from django.urls import path
from .views import (
    NoteListView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    CategoryCreateView,
    CategoryListView, UpdateCategoryView, DeleteCategoryView
)

urlpatterns = [
    path('notes/', NoteListView.as_view(), name='note_list'),
    path('notes/create/', NoteCreateView.as_view(), name='create_note'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='update_note'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='delete_note'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='create_category'),
    path('update_category/', UpdateCategoryView.as_view(), name='update_category'),
    path('delete_category/', DeleteCategoryView.as_view(), name='delete_category'),
]