from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.urls import resolve
from . import models, forms
from django.views.generic import View, ListView


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

def home(request):
    """
    View for rendering home for both: authorized and unauthorised users.
    """
    books = models.Book.objects.all()

    # No query
    if 'q' not in request.GET:

        return render(request, 'home.html', {
            'book_list': books,
        })

    search_form = forms.SearchForm(request.GET)

    if search_form.is_valid():

        # Book.objects.annotate(full_name=Concat('author_name', Value(' '), 'author_surname')).filter(full_name='Marian Falski')
        query_str = search_form.cleaned_data['q']
        print(query_str)
        condition = Q(author_surname__icontains=query_str)|Q(author_name__icontains=query_str)|Q(title__icontains=query_str)
        books = books.filter(condition)

    return render(request, 'home.html', {'book_list': books} )


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
        print("request.POST", request.POST, "")
        form = self.form_class(request.POST, request.FILES, instance=obj)
        number_form = forms.ChangePKBookForm(request.POST, request.FILES)
        valid_form = number_form.is_valid()
        number = number_form.cleaned_data['number']
        number_isavailable = models.Book.objects.filter(pk=number).count() == 0

        if form.is_valid() and number_isavailable:
            print("VALIDO")
            obj = form.save(commit=False)
            obj_created = not obj.pk
            if obj_created:
                obj.pk = number
            obj.save()
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

