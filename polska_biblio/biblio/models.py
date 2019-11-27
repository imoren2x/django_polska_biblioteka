from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

DEFAULT_MAX_LENGTH = 1024

BOOK_STATUS_CHOICES = [
    ('AVAILABLE', 'Available'), ('BORROWED', 'Borrowed'), ('MISSING', 'Missing'), ('UNKNOWN', 'Unknown'),
    ('MAINTENANCE', 'Maintenance'), ('NONAVAILABLE', 'Non available'),
]

COLOUR_CHOICES = [
    ('BLUE', 'Blue'),
    ('RED', 'Red'),
    ('YELLOW', 'Yellow'),
    ('ORANGE', 'Orange'),
    ('BLACK', 'Black'),
    ('GREEN', 'Green'),
    ('WHITE', 'White'),
]

CATEGORY_CHOICES = [ 
    ('PW', 'Novel'), ('KP', 'Polish classics'), ('KZ', 'Foreign classics'), ('RZ', 'Different'), 
    ('HS', 'History'), ('BG', 'Biography'), ('DZ', 'children/youth'), ('PZ', 'Poetry'),
    ('DVD', 'DVD'), ('AL', 'Albums'), ('RL', 'Religion'),
]

class Book(models.Model):
    """
    An Book class - to describe book in the system.
    """
    title = models.CharField(blank=False, max_length=DEFAULT_MAX_LENGTH)  # blank default false
    author_name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    author_surname = models.CharField(blank=True, max_length=DEFAULT_MAX_LENGTH)
    publisher_name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    publisher_city = models.CharField(blank=True, max_length=DEFAULT_MAX_LENGTH)
    year_published = models.PositiveSmallIntegerField(blank=True, null=True)
    ISBN = models.CharField(blank=True, max_length=DEFAULT_MAX_LENGTH)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=DEFAULT_MAX_LENGTH)
    status = models.CharField(choices=BOOK_STATUS_CHOICES, max_length=DEFAULT_MAX_LENGTH)
    location = models.CharField(blank=True, max_length=DEFAULT_MAX_LENGTH)
    # colour = models.CharField(choices=COLOUR_CHOICES, blank=True)  # property consequence of category
    # quantity = models.PositiveSmallIntegerField(null=True)
    description = models.TextField(blank=True)
    # front_page = models.ImageField()
    # end_page = models.ImageField()
    notes = models.TextField(blank=True)
    # arrival_date = models.DateField(auto_now_add=True)
    arrival_date = models.DateField(default=date.today)
    dismiss_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=DEFAULT_MAX_LENGTH, default='Polish')
    # related_books = models.ManyToManyField('self')

    def __str__(self):
        return '%(surname)s, %(name)s: %(title)s (%(year)s)' % {
            'surname': self.author_surname,
            'name': self.author_name,
            'title': self.title,
            'year': self.year_published,
        }

    # @property
    def author_full_name(self):
        return '%s %s' % (self.author_name, self.author_surname)

    def get_absolute_url(self):
        return reverse('books', args=[self.pk])

    class Meta:
        ordering = ['pk', 'author_surname', ]
        verbose_name = "Book"
        verbose_name_plural = "Books"


LIBRARY_USER_STATUS_CHOICES = [
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
]

LIBRARY_USER_ROLES = [
    ('ADMIN', 'Admin'),
    ('READER', 'Reader'),
]

class LibraryUser(models.Model):
    """
    Model for the users of the library, either administrator or user.
    """
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    surname = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=LIBRARY_USER_ROLES, max_length=DEFAULT_MAX_LENGTH)
    address = models.TextField()
    telephone = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    notes = models.TextField(blank=True)
    status = models.CharField(choices=LIBRARY_USER_STATUS_CHOICES, max_length=DEFAULT_MAX_LENGTH)
    number_of_incidences = models.PositiveSmallIntegerField(null=True, default=0)


BORROWING_STATES = [
    ('BORROWED', 'Borrowed'), ('RETURNED', 'Returned'), ('OVERDUE', 'Overdue'), ('RENEWED', 'Renewed'),
    ('INCIDENCE', 'Incidence'), 
]

class Borrowing(models.Model):
    """
    Model that stores a library lending.
    """
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    library_user = models.ForeignKey('LibraryUser', on_delete=models.SET_NULL, null=True)
    borrowing_date = models.DateField()
    borrowing_return_date = models.DateField()
    renewed_return_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField()
    # could be determined by rest of attributes
    state = models.CharField(choices=BORROWING_STATES, max_length=DEFAULT_MAX_LENGTH)
    # state = (active, returned, overdue, incidence) # this should be a property
    notes = models.TextField(blank=True)
