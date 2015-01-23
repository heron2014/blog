from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(required=True, help_text='A valid email address, please')
    message = forms.CharField(required=True, widget=forms.Textarea)