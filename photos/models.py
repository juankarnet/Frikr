# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from photos.settings import LICENSES
from photos.validators import badwords_detector

PUBLIC = 'PUB'
PRIVATE = 'PRI'
VISIBILITY = (
    (PUBLIC, 'Public'),
    (PRIVATE, 'Private ')
)

class Photo(models.Model):
    """
    Otros del equipo comentan estado de foto
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True, null=True, default="", validators=[badwords_detector])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    license = models.CharField(max_length=3, choices=LICENSES)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=PUBLIC)

    def __unicode__(self): #0 params method
        return self.name

class Comment(models.Model):
    writer = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)
    subject = models.CharField(max_length=150)
    text_comment = models.TextField(blank=True, null=True, default="", validators=[badwords_detector, MinLengthValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # 0 params method
        return self.subject
