from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from count_app.models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for u in self.fields.values():
            u.widget.attrs.update({'class': 'form-control'})
            

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'
        exclude = ['user', 'bmr', 'bmi']

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
            
class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

class ConsumeForm(forms.ModelForm):
    class Meta:
        model = CalorieConsume
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})