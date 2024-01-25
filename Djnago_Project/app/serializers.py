from rest_framework import serializers
from .models import Genre, Author, Book,User

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorLoginSerializer(serializers.Serializer):

        
        
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

