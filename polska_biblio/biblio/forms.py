from django.conf import settings
from django import forms
from . import models


#
# Forms
#

class BootstrapMixin(forms.BaseForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        exempt_widgets = [forms.CheckboxInput, forms.ClearableFileInput, forms.FileInput, forms.RadioSelect]

        for field_name, field in self.fields.items():
            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()
            if field.required and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['required'] = 'required'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label


class SearchForm(BootstrapMixin, forms.Form):

    q = forms.CharField(
        label='Search'
    )
    # obj_type = forms.ChoiceField(
        # choices=OBJ_TYPE_CHOICES, required=False, label='Type'


class BookForm(forms.ModelForm):

    class Meta:
        model = models.Book
        fields = ['id', 'title', 'author_name', 'author_surname',
                  'publisher_name', 'publisher_city', 'year_published',
                   'ISBN', 'category', 'status', 'location',
                   'description', 'notes', 'language', ]

    # )
