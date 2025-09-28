from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'firstn',
            'placeholder': 'Full Name',
            'required': True,
            'class': '',  # No class on input, but parent div has classes
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'email',
            'placeholder': 'Email',
            'required': True,
            'class': '',
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'id': 'subject',
            'placeholder': 'Subject',
            'required': True,
            'class': '',
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'message',
            'placeholder': 'Write comments',
            'cols': 30,
            'rows': 10,
        }),
        required=False
    )
    captcha = CaptchaField()  
