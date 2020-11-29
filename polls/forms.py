from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Nom Entreprise", max_length=75, required=False)
    sender = forms.EmailField(label="Email", max_length=50, required=True)
    subject = forms.CharField(label="Sujet", max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, max_length=2000, required=True)
