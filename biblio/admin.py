from django.contrib import admin
from biblio.models import Book, LibraryUser, Borrowing

admin.site.register(Book)
admin.site.register(LibraryUser)
admin.site.register(Borrowing)
