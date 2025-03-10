from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from .forms import SignupUserForm,LoginUserForm
from .models import CustomUser

class vista_registro(View):
    def get(self, request):
        form = SignupUserForm()
        return render(request, "registrar.html", {"form": form})

    def post(self, request):
        form = SignupUserForm(request.POST)
        username=request.POST.get("username").lower()
        password=request.POST.get("password")

        if form.is_valid():
            usuario_registrado = form.save()
            messages.success(request, '¡Usuario registrado exitosamente!')
            user=CustomUser.objects.get(username=username)
            user=authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')
        else:
            # Displaying form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{field}: {error}')

            return render(request, "registrar.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.warning(request, "Usuario no encontrado....")
            return redirect("login")

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            # User authenticated, log in the user
            login(request, user)
            return redirect("index")
        else:
            # Authentication failed, show error message
            messages.warning(request, "Algo anda mal...")
    return render(request, "login.html")
