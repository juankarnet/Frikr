# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from photos.models import Photo, Comment
from photos.settings import BADWORDS


class PhotoForm(forms.ModelForm):
    """
    Formulario para el modelo foto
    """
    class Meta:
        model = Photo
        exclude = ['owner']

class CommentForm(forms.ModelForm):
    """
    Formulario lara el modelo comment
    """
    class Meta:
        model = Comment
        exclude = []