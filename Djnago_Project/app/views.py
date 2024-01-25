from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Author,Book,Genre,User
from .serializers import AuthorSerializer, GenreSerializer,BookSerializer,AuthorLoginSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
# from rest_framework import generics

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthorLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username,password)

            author = authenticate(request, username=username, password=password)
            print(author)

            if author is not None and author.is_active:
                login(request, author)
                return Response({'message': 'Author logged in successfully', 'author_id': author.author_id})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




        

class SignupAuthorAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response({'message': 'Author signed up successfully', 'author_id': author.author_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Admin APIs
class AdminGenreAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, genre_id):
        try:
            genre = Genre.objects.get(pk=genre_id)
            genre.delete()
            return Response({'message': 'Genre deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Genre.DoesNotExist:
            return Response({'error': 'Genre not found'}, status=status.HTTP_404_NOT_FOUND)

class AdminAuthorAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def get_author_details(self, author_id):
        try:
            author = Author.objects.get(pk=author_id)
            serializer = AuthorSerializer(author)
            return serializer.data
        except Author.DoesNotExist:
            return None

    def get(self, request, author_id):
        author_data = self.get_author_details(author_id)
        if author_data:
            return Response(author_data)
        return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

    def get_books(self, author_id):
        try:
            author = Author.objects.get(pk=author_id)
            books = author.books.all()
            serializer = BookSerializer(books, many=True)
            return serializer.data
        except Author.DoesNotExist:
            return None

    def get(self, request, author_id):
        books_data = self.get_books(author_id)
        if books_data:
            return Response(books_data)
        return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

# Author APIs
class AuthorBookAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, author_id):
        try:
            author = Author.objects.get(pk=author_id)
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=author)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, book_id):
        try:
            author = Author.objects.get(pk=author_id)
            book = author.books.get(pk=book_id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (Author.DoesNotExist, Book.DoesNotExist):
            return Response({'error': 'Author or Book not found'}, status=status.HTTP_404_NOT_FOUND)
