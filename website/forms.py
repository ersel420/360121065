from django import forms

class ContactForm(forms.Form):
	name = forms.CharField(label = "Your name", max_length = 110, widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'style': 'height: 54px;',
        'placeholder': 'Your name',
        'id': 'name',
        'rows': '1',
        'type': 'text',
        'required': '',
    }))
	email = forms.EmailField(label = "Your e-mail", max_length = 150, widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder': 'Your e-mail',
        'style': 'height: 54px',
        'id': 'email',
        'rows': '1',
        'type': 'email',
        'required': '',
    }))
	message = forms.CharField(label = "Your message", max_length = 2000, widget = forms.Textarea(attrs = {
        'class': 'form-control',
        'placeholder': 'Your message',
        'id': 'message',
        'rows': '6',
        'required': '',
    }))

    