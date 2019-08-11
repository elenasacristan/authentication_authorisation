from django import forms
'''the following is needed for the register form'''
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

'''form used to log users in'''
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

'''form to register a new user'''
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    '''inner class to specify the model and the fields that we are going to use'''
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        cleaned_data = super().clean()
        email=self.cleaned_data.get('email')
        username=self.cleaned_data.get('username')

        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email must be unique')
        
        return email
    
    def clean_password2(self):
        cleaned_data = super().clean()
        password1=self.cleaned_data.get('password1')        
        password2=self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise forms.ValidationError("Please confirm your password")
        
        if password1 != password2:
            raise forms.ValidationError("The passwords must match")
        
        return password2
