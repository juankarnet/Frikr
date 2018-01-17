# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from photos.models import Photo, Comment


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'license', 'visibility')
    list_filter = ('license', 'visibility')
    search_fields = ('name', 'description')

    def owner_name(self, obj):
        return obj.owner.first_name + u' ' + obj.owner.last_name
    owner_name.short_description = u'Photo owner'
    owner_name.admin_order_field = 'owner'

    #wide alinear los campos en la misma vertical
    #collapse, contraer el div, y que se pueda abrir.
    fieldsets = (
        (None, {
           'fields': ('name',),
            'classes': ('wide',)
        }),
        ('description & author', {
            'fields' : ('description', 'owner'),
            'classes': ('wide',)
        }),
        ('Extra',{
            'fields': ('url', 'license', 'visibility'),
            'classes': ('wide', 'collapse')
        })
    )
admin.site.register(Photo, PhotoAdmin)

admin.site.register(Comment)