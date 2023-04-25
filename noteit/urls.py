from django.contrib import admin
from django.urls import path

from noteit.views import index, NotesDetailView, NotesCreateView, NotesCategoryCreateView, NotesCategoryListView, NotesCategoryUpdateView, NotesCategoryDeleteView, NoteUpdateView, NoteDeleteView, NotesSearchView

urlpatterns = [
    path('', NotesSearchView.as_view(), name='note-list'),
    path('note/', NotesSearchView.as_view(), name='note-list'),
    path('note/<int:pk>/', NotesDetailView.as_view(), name='note-detail'),
    path('note/create/', NotesCreateView.as_view(), name='note-create'),
    path('category/', NotesCategoryListView.as_view(), name='notecategory-list'),
    path('category/create/', NotesCategoryCreateView.as_view(),
         name='notecategory-create'),
    path('category/<int:pk>/update/', NotesCategoryUpdateView.as_view(),
         name='notecategory-update'),
    path('category/<int:pk>/delete/', NotesCategoryDeleteView.as_view(),
         name='notecategory-delete'),
    path('notes/<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),


]
