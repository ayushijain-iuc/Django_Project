from django.contrib import admin
from .models import Genre, Author, Book

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    #list_display = ('username', 'phone', 'city', 'profile_image')
    #search_fields = ('username', 'phone', 'city')  # Add fields you want to search by
    
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone', 'city', 'profile_image', 'author_id', 'date_joined', 'is_active')
    fieldsets = (
        ('Personal Info', {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone', 'city', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'genre', 'num_pages', 'cover_image')
    #list_filter = ('genre', 'author__city')  # Add filters based on your needs



# Register your models here.
