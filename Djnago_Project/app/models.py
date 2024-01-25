from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser,Group, Permission

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Author(AbstractUser):
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='author_profiles/', null=True, blank=True)
    author_id = models.CharField(max_length=20, unique=True, editable=False)
    
    groups = models.ManyToManyField(Group, related_query_name='author', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_query_name='author', blank=True)

    def save(self, *args, **kwargs):
        if not self.author_id:
            # Generate author_id based on the provided format
            city_code = self.city[:3].upper()
            existing_authors = Author.objects.filter(city=self.city)
            new_author_number = existing_authors.count() + 1
            self.author_id = f'AR{city_code}{new_author_number:04d}'

        super(Author, self).save(*args, **kwargs)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    name = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    num_pages = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    
# class login(models.Model):
#     username=models.CharField(max_length=100)
#     password=models.CharField(max_length=10)
