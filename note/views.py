from django.shortcuts import render, redirect
from .models import Note, Category
from .forms import NoteForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.text = request.POST.get('text')
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm(user=request.user)
    return render(request, 'notes/create_note.html', {'form': form})


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('create_note')
    else:
        form = CategoryForm()

    categories = Category.objects.filter(user=request.user)
    return render(request, 'notes/create_category.html', {'form': form, 'categories': categories})


@login_required
def note_list(request):
    query = request.GET.get('query')
    category_id = request.GET.get('category')
    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(text__icontains=query))
    if category_id:
        notes = notes.filter(category_id=category_id)

    categories = Category.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes, 'categories': categories})


@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'notes/category_list.html', {'categories': categories})
