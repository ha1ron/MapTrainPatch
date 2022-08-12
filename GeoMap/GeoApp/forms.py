import datetime
from django import forms
from django.forms import SelectDateWidget


class GetPoezd(forms.Form):
    month = forms.CharField(label='Период', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'month',
                                                                          'placeholder': 'YYYY-MM',
                                                                          'pattern': '[0-9]{4}-[0-9]{2}'}))
    poezd = forms.CharField(max_length=16, label='Поезд', widget=forms.TextInput(attrs={'class': 'form-control'}))
    st_text = forms.BooleanField(label='Тексты', label_suffix=" : ",
                                 required=False, disabled=False,
                                 widget=forms.widgets.CheckboxInput(attrs={'class': 'checkbox-inline'}),
                                 help_text="...",
                                 error_messages={'required': "Please check the box"})


class GetUno(forms.Form):
    month = forms.CharField(label='Период', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'month',
                                                                          'placeholder': 'YYYY-MM',
                                                                          'pattern': '[0-9]{4}-[0-9]{2}'}))
    uno = forms.CharField(max_length=12, label='УНО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    iddos = forms.CharField(max_length=10, label='ID досылки', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
