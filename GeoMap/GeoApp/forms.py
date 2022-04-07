import datetime
from django import forms
from django.forms import SelectDateWidget


class getPoezd(forms.Form):
    month = forms.CharField(label='Период', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'month',
                                                                          'placeholder': 'YYYY-MM',
                                                                          'pattern': '[0-9]{4}-[0-9]{2}'}))
    poezd = forms.CharField(max_length=16, label='Поезд', widget=forms.TextInput(attrs={'class': 'form-control'}))
