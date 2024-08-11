from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Note, Category
from .forms import NoteForm, CategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import UserIsOwnerMixin


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/note_list.html'
    paginate_by = 3  # Number of notes per page

    def get_queryset(self):
        query = self.request.GET.get('query')
        category_id = self.request.GET.get('category')
        notes = Note.objects.filter(user=self.request.user)

        if query:
            notes = notes.filter(Q(title__icontains=query) | Q(text__icontains=query))
        if category_id:
            notes = notes.filter(category_id=category_id)
        return notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(user=self.request.user)
        paginator_categories = Paginator(categories, self.paginate_by)
        paginator_notes = Paginator(self.get_queryset(), self.paginate_by)
        page_number_category = self.request.GET.get('category_page')
        page_number_note = self.request.GET.get('notes_page')
        context['categories_page_obj'] = paginator_categories.get_page(page_number_category)
        context['notes_page_obj'] = paginator_notes.get_page(page_number_note)

        context['categories'] = categories
        print(context)
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/create_note.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NoteUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/update_note.html'
    success_url = reverse_lazy('note_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NoteDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Note
    template_name = 'notes/delete_note.html'
    success_url = reverse_lazy('note_list')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'notes/create_category.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'notes/category_list.html'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

@method_decorator(csrf_protect, name='dispatch')
class UpdateCategoryView(View):
    def post(self, request, *args, **kwargs):
        print("UpdateCategoryView")
        category_id = request.POST.get('id')
        new_name = request.POST.get('name')
        try:
            category = Category.objects.get(id=category_id)
            category.name = new_name
            category.save()
            return JsonResponse({'success': True})
        except Category.DoesNotExist:
            return JsonResponse({'success': False}, status=404)

@method_decorator(csrf_protect, name='dispatch')
class DeleteCategoryView(View):
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('id')
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({'success': True})
        except Category.DoesNotExist:
            return JsonResponse({'success': False}, status=404)