from django.shortcuts import render,redirect
from .forms import formContacto
from django.core.mail import EmailMessage

# Create your views here.
def contacto(request):
    formulario_contacto=formContacto()

    if request.method=="POST":
        formulario_contacto=formContacto(data=request.POST)

        if formulario_contacto.is_valid():
            nombre=request.POST.get("nombre")
            mail=request.POST.get("mail")
            contenido=request.POST.get("contenido")

            mail=EmailMessage(
                "Mensaje desde App Django",
                f"{nombre} ({mail}): {contenido}",
                "",
                ["ds.diegodsm@gmail.com"],
                reply_to=[mail]
            )
            try:
                mail.send()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?novalido")

    return render(request, "contacto.html",{"formulario":formulario_contacto})
