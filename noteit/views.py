from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Note, NoteCategory


# Create your views here.


def index(request):
    return render(request, 'account/login.html')


@method_decorator(login_required, name='dispatch')
class NotesListView(ListView):
    model = Note
    context_object_name = 'notes'
    ordering = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(assigned_to=self.request.user)


@method_decorator(login_required, name='dispatch')
class NotesDetailView(DetailView):
    model = Note


@method_decorator(login_required, name='dispatch')
class NotesCreateView(CreateView):
    model = Note
    fields = ['name', 'description', 'category', 'note_img']
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.assigned_to = self.request.user
        form.instance.note_img = self.request.FILES.get('note_img')
        return super(NotesCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class NotesCategoryListView(ListView):
    model = NoteCategory
    context_object_name = 'categories'


@method_decorator(login_required, name='dispatch')
class NotesCategoryCreateView(CreateView):
    model = NoteCategory
    fields = ['name']

    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NotesCategoryCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class NotesCategoryUpdateView(UpdateView):
    model = NoteCategory
    fields = ['name']
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NotesCategoryDeleteView(DeleteView):
    model = NoteCategory
    success_url = reverse_lazy('note-list')


@method_decorator(login_required, name='dispatch')
class NoteUpdateView(UpdateView):
    model = Note
    fields = ['name', 'description', 'category', 'note_img']
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')


@method_decorator(login_required, name='dispatch')
class NotesSearchView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if category:
            queryset = queryset.filter(category__name__iexact=category)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(assigned_to__username__icontains=query)
            )

        if not user.is_superuser:
            queryset = queryset.filter(assigned_to=user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        notes = context['notes']

        for i, note in enumerate(notes):

            note.short_description = note.description[:180] + '...' if len(
                note.description) > 180 else note.description
            note.index = i + 1

        categories = NoteCategory.objects.all()
        selected_category = self.request.GET.get('category', '')

        context.update({
            'categories': categories,
            'selected_category': selected_category,
        })

        return context
