import csv
import datetime

from django.shortcuts import render

# Create your views here.
from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, render, redirect
# from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.urls import resolve
from . import models, forms
from django.views.generic import View, ListView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from polska_biblio import settings

class GetReturnURLMixin(object):
    """
    Provides logic for determining where a user should be redirected after processing a form.
    """
    default_return_url = None

    def get_return_url(self, request, obj):
        query_param = request.GET.get('return_url')
        if query_param and is_safe_url(url=query_param, host=request.get_host()):
            return query_param
        elif obj.pk and hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()
        elif self.default_return_url is not None:
            return reverse(self.default_return_url)
        return reverse('home')


# Create your views here.

def about(request, *args, **kwargs):

    return render(request, 'about.html', {
            'version': settings.VERSION,
        })

def home(request, *args, **kwargs):
    """
    View for rendering home for both: authorized and unauthorised users.
    """
    books = models.Book.objects.annotate(full_name=Concat('author_name', Value(' '), 'author_surname')).all()
    available_count = books.filter(status='AVAILABLE').count()
    borrowed_count = books.filter(status='BORROWED').count()

    full_catalog = True if request.GET.get('full_catalog', '').lower() == 'true' else False
    if full_catalog is False:
        books = books.order_by('-id')[0:500+1]

    # No query
    if 'q' not in request.GET:

        return render(request, 'home.html', {
            'book_list': books,
            'available_count': available_count,
            'borrowed_count': borrowed_count,
            'search': False,
            'full_catalog': full_catalog,
            'version': settings.VERSION,
        })

    search_form = forms.SearchForm(request.GET)

    if search_form.is_valid():

        query_str = search_form.cleaned_data['q'].strip()
        # author
        Q_author = Q(full_name__icontains=query_str)
        # title
        Q_title = Q(title__icontains=query_str)
        # publisher
        Q_publisher = Q(publisher_name__icontains=query_str)
        # year_published
        Q_year_published = Q(year_published__icontains=query_str)
        # ISBN
        Q_ISBN = Q(ISBN__icontains=query_str)
        # category
        Q_category = Q(category__icontains=query_str)
        # status
        Q_status = Q(status__icontains=query_str)
        # location
        Q_location = Q(location__icontains=query_str)
        # language
        Q_language = Q(language__icontains=query_str)
        
        books = books.filter(
                Q_author|Q_title|Q_publisher|Q_year_published|
                Q_ISBN|Q_category|Q_status|Q_location|Q_language
            )

    return render(request, 'home.html', {
                    'book_list': books,
                    'search': True,
                    'version': settings.VERSION,
                 })


def backup_json(request):

    response = JsonResponse([dict(book) for book in models.Book.objects.all().values()], safe=False)

    strftime = datetime.datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
    filename = "Biblioteka_books_%s.json" % strftime

    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    return response

# class Echo:
    # """An object that implements just the write method of the file-like
    # interface.
    # """
    # def write(self, value):
        # """Write the value by returning it, instead of storing in a buffer."""
        # return value


# def backup_csv(request):
    # """A view that streams a large CSV file."""
    # # Generate a sequence of rows. The range is based on the maximum number of
    # # rows that can be handled by a single sheet in most spreadsheet
    # # applications.
    # # # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    # header = ['pk', 'title', 'author_name', 'author_surname', 'publisher_name', 'publisher_city', 'year_published', 'ISBN', 'category', 'status', 'location', 'description', 'notes', 'arrival_date', 'dismiss_date', 'language', ]
    # rows = (header, 
    # pseudo_buffer = Echo()
    # writer = csv.writer(pseudo_buffer)
    # response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     # content_type="text/csv")
    # response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    # return response


def book_author(request, *args, **kwargs):

    pk = kwargs.get('pk')
    author_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(
            author_name=author_book.author_name,
            author_surname=author_book.author_surname,
        )

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })

def publisher_name(request, *args, **kwargs):

    pk = kwargs.get('pk')
    publisher_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(publisher_name=publisher_book.publisher_name)

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })

def publisher_city(request, *args, **kwargs):

    pk = kwargs.get('pk')
    city_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(publisher_city=city_book.publisher_city)

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })

def year_published(request, *args, **kwargs):

    pk = kwargs.get('pk')
    year_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(year_published=year_book.year_published)

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })

def status(request, *args, **kwargs):

    pk = kwargs.get('pk')
    status_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(status=status_book.status)

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })

def category(request, *args, **kwargs):

    pk = kwargs.get('pk')
    category_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(category=category_book.category)

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })

def location(request, *args, **kwargs):

    pk = kwargs.get('pk')
    location_book = models.Book.objects.get(pk=pk)
    
    books = models.Book.objects.filter(location=location_book.location)

    return render(request, 'home.html', {
        'book_list': books,
        'search': True,
    })


class BookView(View):

    def get(self, request, pk, *args, **kwargs):

        book = get_object_or_404(models.Book, pk=pk)

        return render(request, 'books/book.html', {
            'book': book,
        })


class BookEditView(GetReturnURLMixin, View):
    """
    Create or edit a single book.
    """
    model = models.Book
    form_class = forms.BookForm
    fields_initial = []
    template_name = 'books/book_edit.html'
    # default_return_url = 'home'
    default_return_url = 'book'

    def get_object(self, kwargs):
        # Look up object by slug or PK. Return None if neither was provided.
        if 'slug' in kwargs:
            return get_object_or_404(self.model, slug=kwargs['slug'])
        elif 'pk' in kwargs:
            return get_object_or_404(self.model, pk=kwargs['pk'])
        return self.model()

    def get(self, request, *args, **kwargs):

        number_form = None
        book = self.get_object(kwargs)
        if not book.id:
            number_form = forms.ChangePKBookForm()
            number_form.fields['number'].label = "Number"

        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}

        form = self.form_class(instance=book, initial=initial_data)

        return_url = reverse('book', args=[book.pk]) if book.pk else reverse('home')

        return render(request, self.template_name, {
            'book': book,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'number_form': number_form,
            'return_url': return_url,
        })

    def post(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj_created = not obj.pk
        print("request.POST", request.POST, "")
        form = self.form_class(request.POST, request.FILES, instance=obj)
        # if add view
        if obj_created:
            number_form = forms.ChangePKBookForm(request.POST, request.FILES)

            valid_form = number_form.is_valid()
            if valid_form:
                number = number_form.cleaned_data['number']
                number_isavailable = models.Book.objects.filter(pk=number).count() == 0
            else:
                number_isavailable = False
                number = None
        else:
            number_form = None

        # edit
        if not obj_created and form.is_valid():
            print("VALIDO")
            obj = form.save(commit=False)
            obj.save()

            return redirect(self.default_return_url, obj.pk)

        # add
        elif obj_created and valid_form and form.is_valid() and number_isavailable:
            print("VALIDO")
            obj = form.save(commit=False)
            if obj_created:
                obj.pk = number

            return redirect(self.default_return_url, obj.pk)

        else:
            print("NO VALIDO")
            print("form.errors", form.errors, "")
            print("form.non_field_errors", form.non_field_errors(), "")

        return render(request, self.template_name, {
            'form': form,
            'number_form': number_form,
            'number_invalid': not number_isavailable,
            'number': number,
            'return_url': reverse('home'),
        })


class ChangePKBookView(BookEditView):
    """
    """
    model = models.Book
    form_class = forms.ChangePKBookForm
    template_name = 'books/book_changepk.html'
    default_return_url = 'book'

    def get(self, request, *args, **kwargs):

        book = self.get_object(kwargs)
        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}

        if book.id:
            initial_data.update({'number': book.pk})
        form = self.form_class(initial=initial_data)

        return_url = reverse('book', args=[book.pk]) if book.pk else reverse('home')

        return render(request, self.template_name, {
            'book': book,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': return_url,
        })

    def post(self, request, *args, **kwargs):

        book = self.get_object(kwargs)
        # print("request.POST", request.POST, "")
        form = self.form_class(request.POST, request.FILES)
        valid_form = form.is_valid()
        new_pk = form.cleaned_data['number']
        new_pk_isavailable = models.Book.objects.filter(pk=new_pk).count() == 0
        if valid_form and new_pk_isavailable:
            # print("VALIDO")
            # obj = form.save(commit=False)
            new_book = book
            book.delete()
            new_book.pk = new_pk
            # obj_created = not obj.pk
            new_book.save()
            book = new_book
            return redirect(self.default_return_url, new_book.pk)
        else:
            print("NO VALIDO")
            print("form.errors", form.errors, "")
            print("form.non_field_errors", form.non_field_errors(), "")

        return render(request, self.template_name, {
            'form': form,
            'new_pk': new_pk,
            'new_pk_invalid': not new_pk_isavailable,
            'book': book,
            'return_url': reverse('home'),
        })


class BookDelView(BookEditView):
    """
    """
    model = models.Book
    form_class = forms.ChangePKBookForm
    template_name = 'books/book.html'
    template_return = 'home.html'
    default_return_url = 'book'

    def get(self, request, *args, **kwargs):

        book = self.get_object(kwargs)

        return render(request, self.template_name, {
            'book': book,
            'obj_type': self.model._meta.verbose_name,
            'return_url': reverse(self.default_return_url, args=[book.pk]),
            'delete': True,
        })

    def post(self, request, *args, **kwargs):

        book = self.get_object(kwargs)
        print("request.POST", request.POST, "")
        # import pdb; pdb.set_trace()

        deleted_number = book.pk
        book.delete()
        messages.success(request,
                "Book number %s, %s, has been successfully deleted." % (deleted_number, str(book))
            )

        return redirect('home')
