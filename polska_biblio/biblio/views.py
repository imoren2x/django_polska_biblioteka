from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
# from django.core.urlresolvers import reverse
from django.urls import reverse
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
        
        query_str = search_form.cleaned_data['q']

        books = books.filter(author_surname__icontains=query_str)

    return render(request, 'home.html', {'book_list': books} )


class BookView(View):

    def get(self, request, pk):

        book = get_object_or_404(models.Book, pk=pk)

        return render(request, 'books/book.html', {
            'book': book,
        })


class BookEditView(GetReturnURLMixin, View):
    """
    Create or edit a single TradeModel.
    """
    model = models.Book
    form_class = forms.BookForm
    fields_initial = []
    template_name = 'books/book_edit.html'
    default_return_url = 'home'

    def get_object(self, kwargs):
        # Look up object by slug or PK. Return None if neither was provided.
        if 'slug' in kwargs:
            return get_object_or_404(self.model, slug=kwargs['slug'])
        elif 'pk' in kwargs:
            return get_object_or_404(self.model, pk=kwargs['pk'])
        return self.model()

    def get(self, request, *args, **kwargs):

        book = self.get_object(kwargs)
        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}

        form = self.form_class(instance=book, initial=initial_data)

        return render(request, self.template_name, {
            'book': book,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': reverse(self.default_return_url),
        })

    def post(self, request, *args, **kwargs):

        print("request.POST", request.POST, "")
        form = self.form_class(request.POST)

        if form.is_valid():
            print("VALIDO")
            obj = form.save(commit=False)
            obj_created = not obj.pk
            obj.save()
            return redirect(reverse(self.default_return_url),)
        else:
            print("NO VALIDO")
            print("form.errors", form.errors, "")
            print("form.non_field_errors", form.non_field_errors(), "")

        return render(request, self.template_name, {
            'form': form,
            'return_url': reverse(self.default_return_url),
        })

