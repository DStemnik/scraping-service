from django import forms
from scraping.models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=False,
                                  widget=forms.Select(attrs={'class': 'form-select my-1'}),
                                  label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name='slug',
                                      required=False,
                                      widget=forms.Select(attrs={'class': 'form-select my-1'}),
                                      label='Язык программирования')
