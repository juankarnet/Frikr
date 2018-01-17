from rest_framework import serializers
from models import Photo, Comment


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        exclude = []
        read_only_fields = ['owner']


class PhotoListSerializer(PhotoSerializer):

    class Meta(PhotoSerializer.Meta):
        fields = ('id', 'name', 'url')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = []
