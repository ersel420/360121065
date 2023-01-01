from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordResetForm, SetPasswordForm

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label = 'Enter Username', min_length = 3, max_length = 50, help_text = 'Required')
    email = forms.EmailField(label = 'Enter E-Mail', max_length = 100, help_text = 'Required', error_messages = {
        'required': 'You need to have an e-mail'
    })
    password = forms.CharField(label = 'Enter Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Repeat Password', widget = forms.PasswordInput)
    firstName = forms.CharField(label = 'Enter First Name', max_length = 50)
    lastName = forms.CharField(label = 'Enter Last Name', max_length = 50)
    phoneNumber = forms.CharField(label = 'Enter Phone Number', max_length = 11)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'password', 'firstName', 'lastName', 'phoneNumber',)

    def isUsernameExists(self): #Username Existance Control
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name = user_name)
        if r.count():
            raise forms.ValidationError("This username is already exists.")
        return user_name

    def isEmailExists(self): #Email Existance Control
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email = email).exists():
            raise forms.ValidationError("This e-mail address is already exists.")
        return email

    def pwdControl(self): #Password Match
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match.")
        return cd['password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'E-Mail',
        'id': 'login-username',
        'required': '',
    }))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Password',
        'type': 'password',
        'id': 'login-pwd',
        'required': '',
    }))

class UserEditForm(UserChangeForm):
    email = forms.EmailField(label = 'Email', max_length = 100, widget = forms.TextInput(attrs = {
        'class': 'col-md-12',
        'placeholder': 'E-Mail Address',
        'id': 'form-email',
        'readonly': 'readonly',
    }))
    user_name = forms.CharField(label = 'Username', min_length = 4, max_length = 50, widget = forms.TextInput(attrs = {
        'class': 'col-md-12',
        'placeholder': 'Username',
        'id': 'form-username',
    }))
    phoneNumber = forms.CharField(label = 'Phone Number', min_length = 11, max_length = 11, widget = forms.TextInput(attrs = {
        'class': 'col-md-12',
        'placeholder': 'Phone Number',
        'id': 'form-phone',
        
    }))
    address = forms.CharField(label = 'Address', max_length = 500, widget = forms.TextInput(attrs = {
        'class': 'col-md-12',
        'placeholder': 'Address',
        'id': 'form-address',
    }))
    firstName = forms.CharField(label = 'First Name', max_length = 50, widget = forms.TextInput(attrs = {
        'class': 'col-md-12',
        'placeholder': 'First Name',
        'id': 'form-fname',
    }))
    lastName = forms.CharField(label = 'Last Name', max_length = 50, widget = forms.TextInput(attrs = {
        'class': 'col-md-12',
        'placeholder': 'Last Name',
        'id': 'form-lname',
    }))

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'password', 'firstName', 'lastName', 'phoneNumber', 'address',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True

class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length = 100, widget = forms.TextInput(attrs = {
        'class': 'form-control',
        'placeholder': 'E-Mail',
        'id': 'pwdchange-mail',
        'required': '',
    }))

    def checkMail(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email = email)
        if not u:
            raise forms.ValidationError('We cannot find this e-mail address.')
        return email

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label = "New Password", widget = forms.PasswordInput(attrs = {
        'class': 'form-control',
        'placeholder': 'New Password',
        'type': 'password',
        'id': 'new-pwd',
        'required': '',
    }))
    new_password2 = forms.CharField(label = "Repeat New Password", widget = forms.PasswordInput(attrs = {
        'class': 'form-control',
        'placeholder': 'Repeat New Password',
        'type': 'password',
        'id': 'new-pwd-2',
        'required': '',
    }))