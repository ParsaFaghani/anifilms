from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm


#using first_name as full_name 
class SignupForm(UserCreationForm):
    username   = forms.CharField(widget=(forms.TextInput(attrs={'class': 'border rounded w-full py-2 px-3', 'placeholder': _('enter username')})),label='')
    first_name = forms.CharField(widget=(forms.TextInput(attrs={'class': 'border rounded w-full py-2 px-3', 'placeholder': _('enter first name')})),label='', max_length=32)
    email      = forms.EmailField(widget=(forms.EmailInput(attrs={'class': 'border rounded w-full py-2 px-3', 'placeholder': _('enter email')})),label='', max_length=64)
    password1  = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'border rounded w-full py-2 px-3', 'placeholder': _('enter password')})),label='')
    password2  = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'border rounded w-full py-2 px-3', 'placeholder': _('enter repeat the password')})),label='')

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Another account is using {email}")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username isn't available. Please try another.")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('email', 'first_name','username', 'password1','password2')


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=(forms.TextInput(attrs={'class': 'signup-form', 'placeholder': 'Username'})),label='')
    password = forms.CharField(widget=(forms.PasswordInput(attrs={'class': 'signup-form', 'placeholder': 'Password'})),label='')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'user-edit-form','placeholder': 'Name'},)
        self.fields['first_name'].label = 'Name'
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'user-edit-form','placeholder': 'Username'},)
        self.fields['username'].help_text = None
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'user-edit-form','placeholder': 'Email'},)
        self.fields['email'].label = 'Email'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','photo']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        self.fields['bio'].widget = forms.TextInput(attrs={'class': 'user-edit-form','placeholder': 'Bio'},)


class passwordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(passwordChangeForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'text-gray-800','placeholder': 'current passowrd'},)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'text-gray-800','placeholder': 'new passowrd'},)
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'text-gray-800','placeholder': 'confirm passowrd'},)

