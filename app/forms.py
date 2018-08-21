# # -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
import datetime

from app.models import User

# from app.app

class SignUpForm(UserCreationForm):

  first_name = forms.CharField(max_length=30, required=True, label='Nombre')
  last_name = forms.CharField(max_length=30, required=True, label='Apellido')
  # mobile_phone = forms.RegexField(regex=r'^\+?\d{9,15}$', required=True, label="Número de teléfono ( Ej +582125834456 )")
  # address = forms.CharField(max_length=30, required=True, label='Dirección')
  id_number = forms.CharField(max_length=30, required=True, label='Número de identificación')

  def __init__(self, *args, **kwargs):
    super(SignUpForm, self).__init__(*args, **kwargs)
    for i in self.fields:
        self.fields[i].widget.attrs.update({'class' : 'form-control', 'placeholder': self.fields[i].label})
  
  def clean_email(self):
    return self.cleaned_data['email'].lower()
  
  def clean_first_name(self):
    return self.cleaned_data['first_name'].title()
  
  def clean_last_name(self):
    return self.cleaned_data['last_name'].title()

  class Meta:
    model = User
    fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'id_number')



# class AuthenticationForm(forms.Form):

#   email = forms.EmailField(required=True, label=_(u"Email"))
#   password = forms.CharField(widget=forms.PasswordInput, required=True, label=_(u"Password"))

#   def __init__(self, *args, **kwargs):
#     super(AuthenticationForm, self).__init__(*args, **kwargs)
#     for i in self.fields:
#         self.fields[i].widget.attrs.update({'class' : 'form-control', 'placeholder': self.fields[i].label})


class iniciarSesionForm(forms.Form):
    identificacion = forms.CharField(
                            max_length = 50,
                            required = True,
                            label = "Usuario",
                            widget = forms.TextInput(attrs={'style': 'width:100%'})
                    )

    clave = forms.CharField(
                            max_length = 25,
                            required = True,
                            label = "Contraseña",
                            widget = forms.PasswordInput(attrs={'style': 'width:100%'})
            )


class cargarImagenesVueloForm(forms.Form):
    archivo = forms.FileField(required=True)
    

