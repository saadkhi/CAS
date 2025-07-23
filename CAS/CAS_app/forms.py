from django import forms

class NewsletterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email',
        'class': 'px-3 py-2 text-sm text-gray-800 border border-gray-300 rounded focus:outline-none w-full'
    }))