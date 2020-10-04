from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Nom Entreprise", required=False)
    sender = forms.EmailField(label="Email", required=True)
    subject = forms.CharField(label="Sujet", max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
