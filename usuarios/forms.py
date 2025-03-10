from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class SignupUserForm(forms.ModelForm):
    gender_choices=(
        ('','Elige una opcion'),
        ('m',"Masculino"),
        ("f","Femenino"),
    )
    altura = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu altura:'})
    )
    peso = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu peso:'})
    )

    edad = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu edad:'})
    )

    genero=forms.ChoiceField(
        choices=gender_choices,
        widget=forms.Select(attrs={'class':"form-control", "aria-label":"Default select example"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'altura', 'peso', 'genero','edad')

    def save(self, commit=True):
        user = super(SignupUserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password:  # Check if password is provided
            user.set_password(password)  # Hash the password
        if commit:
            user.save()
        return user


class LoginUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=('username', 'password')
