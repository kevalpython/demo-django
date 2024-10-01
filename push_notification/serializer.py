from django.urls import include, path
from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelField):
    class Meta:
        model = Book
        fields = ["author", "book"]
