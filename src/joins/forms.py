from django import forms
from .models import Join

# this is method using django forms
# class EmailForm(forms.Form):
#     email = forms.EmailField()

# this is method using model forms
class JoinForm(forms.ModelForm):
    class Meta:
        model = Join
        fields = ["email",]