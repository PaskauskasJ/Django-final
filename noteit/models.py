from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class NoteCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Note(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    category = models.ForeignKey(NoteCategory, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note_img = models.ImageField(upload_to='img/', blank=True, null=True)

    def __str__(self):
        return self.name
