"""polska_biblio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import biblio.views

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path(r'logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_REDIRECT_URL), name='logout'),
    path(r'', biblio.views.home, name='home'),
    path(r'search/', biblio.views.home, name='search'),
    # path(r'search/', biblio.views.SearchView.as_view(), name='search'),
    path(r'about/', biblio.views.about, name='about'),

    path(r'books/<int:pk>/', biblio.views.BookView.as_view(), name='book'),
    path(r'books/add/', biblio.views.BookEditView.as_view(), name='book_add'),
    path(r'books/<int:pk>/edit/', biblio.views.BookEditView.as_view(), name='book_edit'),
    path(r'books/changepk/<int:pk>/', biblio.views.ChangePKBookView.as_view(), name='changepk'),
    path(r'books/delete/<int:pk>/', biblio.views.BookDelView.as_view(), name='book_del'),
    path(r'books/author/<int:pk>/', biblio.views.book_author, name='author'),
    path(r'books/publisher_name/<int:pk>/', biblio.views.publisher_name, name='publisher_name'),
    path(r'books/publisher_city/<int:pk>/', biblio.views.publisher_city, name='publisher_city'),
    path(r'books/year_published/<int:pk>/', biblio.views.year_published, name='year_published'),
    path(r'books/status/<int:pk>/', biblio.views.status, name='status'),
    path(r'books/category/<int:pk>/', biblio.views.category, name='category'),
    path(r'books/location/<int:pk>/', biblio.views.location, name='location'),

    path(r'backup_json/', biblio.views.backup_json, name='backup_json'),

]
