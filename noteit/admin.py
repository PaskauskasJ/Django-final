from django.contrib import admin
from .models import NoteCategory, Note

# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Note._meta.fields]


admin.site.register(Note, NoteAdmin)

admin.site.register(NoteCategory)
