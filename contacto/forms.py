from django import forms

class formContacto(forms.Form):
    nombre=forms.CharField(label="Nombre", required=True)
    mail=forms.CharField(label="Mail", required=True)
    contenido=forms.CharField(label="Contenido",widget=forms.Textarea)
