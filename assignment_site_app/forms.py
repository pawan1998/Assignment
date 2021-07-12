from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from assignment_site_app.models import UserSearchDetails

# class DetailForm(forms.Form):
#     name = forms.CharField(max_length=50)
#     mail = forms.EmailField(max_length=50)
#     age = forms.CharField(max_length=50)
#     city = forms.CharField(max_length=50)
#     state = forms.CharField(max_length=50) 
#     zips = forms.CharField(max_length=50)


class CreateUserForm(UserCreationForm):
    
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Enter email', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Enter Password', min_length=4, max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Enter email', min_length=4, max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control'}))   
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUserForm(forms.Form):
    
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Enter Password', min_length=4, max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control'}))

# class UserCreationForm(forms.Form):
    
#     username = forms.CharField(label='Enter Username', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
#     email = forms.EmailField(label='Enter email', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
#     password1 = forms.CharField(label='Enter Password', min_length=4, max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password2 = forms.CharField(label='Enter email', min_length=4, max_length=150, widget=forms.PasswordInput(attrs={'class':'form-control'}))   
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
 