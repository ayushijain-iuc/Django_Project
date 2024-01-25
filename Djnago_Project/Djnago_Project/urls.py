from django.contrib import admin
from django.urls import path, include
from app.views import LoginAPI, SignupAuthorAPI, AdminGenreAPI, AdminAuthorAPI, AuthorBookAPI
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginAPI.as_view(), name='login'),
    path('signup/', SignupAuthorAPI.as_view(), name='signup_author'),
    path('admin/genre/', AdminGenreAPI.as_view(), name='admin_genre'),
    path('admin/author/', AdminAuthorAPI.as_view(), name='admin_author'),
    path('author/book/', AuthorBookAPI.as_view(), name='author_book'),
    # Include an 'id' parameter for AdminAuthorAPI
    path('admin/author/<int:id>/', AdminAuthorAPI.as_view(), name='admin_author_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
