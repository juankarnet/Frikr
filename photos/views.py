# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from photos.forms import PhotoForm
from photos.models import Photo, PUBLIC, Comment

from django.views.generic import View, ListView

from django.utils.decorators import method_decorator

class Photos_Queryset(object):

    def get_photos_queryset(self, request):
        if not request.user.is_authenticated():
            photos = Photo.objects.filter(visibility=PUBLIC)
        elif request.user.is_superuser: #Si es administrador
            photos = Photo.objects.all()
        else:
            photos = Photo.objects.filter(Q(owner = request.user)| Q(visibility= PUBLIC))
        return photos


class HomeView(View):
    def get(self, request):

        photos = Photo.objects.filter(visibility=PUBLIC).select_related('owner').order_by('-created_at')
        templateN = 'photos/home.html'
        context = {
            'photos_list' : photos[:5]
        }
        return render(request, templateN, context)
        #html = "<ul>";
        #for photo in photos:
        #    html += "<li>" + photo.name + "</li>";

        #html += "</ul>";

        #return HttpResponse(html)

class DetailView(View, Photos_Queryset):

    def get(self, request, pk):
        """
        Carga la página de detalles de una foto
        :param request: HttpRequest
        :param pk: id de la foto
        :return: HttpResponse
        """
        templateD = 'photos/detail.html'

        possible_photos = self.get_photos_queryset(request).filter(pk=pk).select_related('owner')
        photo = possible_photos[0] if len(possible_photos) == 1 else None

        comments = Comment.objects.all().filter(photo=photo)
        
        if photo is not None:
            #Carga la plantilla de detalle
            context = {
                'photo': photo,
                'comments': comments
            }
            return render(request, templateD, context)
        else:
            return HttpResponseNotFound("No existe la foto"); #404 Not found

class OnlyAuthenticatedView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return super(OnlyAuthenticatedView, self).get(request)


class CreateView(View):


    @method_decorator(login_required())
    def get(self, request):
        """
        Method to show the form to add a photo.
        :param request:
        :return:
        """
        form = PhotoForm()
        context = {
            'form': form,
            'success_message': ''
        }

        return render(request, 'photos/new_photo.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Method to add a photo in an user.
        :param request:
        :return:
        """
        success_message = ''

        photo_with_owner = Photo()
        photo_with_owner.owner = request.user #Se asigna como propietario el usuario logado.
        form = PhotoForm(request.POST, instance=photo_with_owner)
        if form.is_valid():
            new_photo = form.save() # Save the form and return it
            form = PhotoForm() # Inicialize the form empty
            success_message= 'Guardado con éxito!'
            success_message+='<a href="' + reverse('photo_detail', args=[new_photo.pk]) + '" >'
            success_message+='Ver foto'
            success_message+='</a>'
        context = {
            'form': form,
            'success_message': success_message
        }

        return render(request, 'photos/new_photo.html', context)

class PhotoListView(View, Photos_Queryset):
    def get(self, request):
        """
        Devuelve las fotos publicas si el usuario no está autenticado.
        Las fotos del usuario autenticado o las publicas de otros.
        Si el usuario es superadministrador, todas las fotos.
        :param request:
        :return:
        """

        context = {
            'photos': self.get_photos_queryset(request)
        }

        return render(request, 'photos/photos_list.html', context)

class UserPhotosView(ListView):
    model = Photo
    template_name = 'photos/user_photos.html'

    def get_queryset(self):
        queryset = super(UserPhotosView, self).get_queryset()
        return queryset.filter(owner=self.request.user)

class UserPhotoCommentView():
    model = Comment
    template_name = ''