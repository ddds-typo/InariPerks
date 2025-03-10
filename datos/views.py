from django.shortcuts import render,redirect
from .models import foodlist,actividades
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def vista_actividades(request):
    #
    usuario = request.user 
    if request.method == "POST":
        input_formulario = request.POST.get("input")
        if input_formulario=="":
            messages.error(request, "No escribiste nada.....")
            return redirect("actividades")

        regex=regex_buscar_actividad(input_formulario)
        try:
            regex_actividad=regex['actividad']
            if regex_actividad=="":
                messages.error(request, "No escribiste actividad.....")
                return redirect("actividades")
        except Exception:
            messages.error(request, "Algo anda mal.....")
            return redirect("actividades")
        
        regex_tiempo=regex['parametros']
        tiempo=sintonizar_tiempo(regex_tiempo)

        filtro = actividades.objects.filter(nombre__icontains=regex_actividad)
        
        resultado=filtro.first()
        if resultado==None:
            messages.error(request, "No existe esa actividad.....")
            return redirect("actividades")

        calorias=round(calcular_calorias(
                usuario.altura,
                usuario.peso,
                usuario.genero,
                usuario.edad,
                resultado.eet,tiempo
            ),2)
        
        julios=round(calorias*4.184,2)
        kcal=round(calorias/1000,4)
        
        return render(request, "actividades.html", {
            "filtro":filtro,
            "resultado":resultado,
            "actividad":regex_actividad,
            "tiempo":regex_tiempo,
            "calorias":calorias,
            "julios":julios,
            "kcal":kcal,
            })
    else:
        return render(request, "actividades.html")
    
def regex_buscar_actividad(clave):
    clave_separada = re.split(r'[,. ]', clave)
    unidades = ["segundos", "seg", "segs", "s", "minutos", "min", "mins", "m", "horas", "h", "segundo", "minuto", "hora"]

    numeros = [value for value in clave_separada if any(char.isdigit() for char in value)]
    unidades_encontradas = [unit for unit in clave_separada if unit in unidades]

    actividad_buscada = " ".join([word for word in clave_separada if word not in numeros and word not in unidades_encontradas])

    parametro_buscado = None
    if numeros and unidades_encontradas:
        parametro_buscado = f"{numeros[0]} {unidades_encontradas[0]}"
    else:
        parametro_buscado = "30 minutos"

    claves_depuradas = {"actividad": actividad_buscada.strip(), "parametros": parametro_buscado}
    return claves_depuradas

def sintonizar_tiempo(tiempo):
    #
    inputs = re.split(" ", tiempo)
    segundos = ["segundos", "segundo", "seg", "segs","s"]
    horas = ["horas","hora", "h"]
    minutos = ["minutos","minuto", "min", "mins", "m"]

    if inputs[1] in segundos:
        x = int(inputs[0]) / 60
    elif inputs[1] in horas:
        x = int(inputs[0]) * 60
    elif inputs[1] in minutos:
        x = int(inputs[0]) * 1

    return x

def calcular_calorias(altura,peso,genero,edad,ee,tiempo):
    eet=ee*tiempo

    numerador=peso**2 * 25.2**-1
    if genero=="m":
        denominador_man=66.473+5.0033*altura+13.7516*peso-6.755*edad
        return eet*numerador/denominador_man
    elif genero=="f":
        denominador_wman=655.096+1.8496*altura+9.5634*peso-4.6756*edad
        return eet*numerador/denominador_wman

def vista_nutricion(request , id=None):
    #
    if id is not None:
        resultado = foodlist.objects.filter(id=id)
        comida_nombre_id=resultado.first().Nombre
        if request.method == "POST":
            try:
                input_data = request.POST.get("input")
                if input_data=="":
                    messages.error(request, "No escribiste nada...")
                    return redirect("nutricion")
                else:
                    return evento_buscar_comida(request,input_data)

            except UnboundLocalError:
                messages.error(request, "No escribiste nada.....")
                return redirect("nutricion")
        else:
            return evento_buscar_comida(request, comida_nombre_id)


    if request.method == "POST":
        try:
            input_data = request.POST.get("input")
            if input_data=="":
                messages.error(request, "No escribiste nada...")
                return redirect("nutricion")
            else:
                return evento_buscar_comida(request,input_data)

        except UnboundLocalError:
            messages.error(request, "No escribiste nada.....")
            return redirect("nutricion")

    else:
        return render(request, "nutricion.html")

def convertir_entrada_lista(input_text,values):
    #
    input_text_split=input_text.split(" ")
    if input_text_split[1] in ["grams","gramos", "g", "gr"]:
        conversor=float(input_text_split[0])/ 100
    elif input_text_split[1] in ["miligrams","miligramos","mg"]:
        conversor=float(input_text_split[0])/ 100000

    numero_crudo=[]
    for el in values:
        regizado=re.sub(r'[^\d.]+', '', el)
        n_convertido=float(regizado)*conversor
        new_data=el.replace(str(regizado),str(n_convertido))
        numero_crudo.append(new_data)
    return numero_crudo

def separar_nombre_unidad(input_text):
    #
    resultado={}
    cantidad = None

    r = re.split(r'[,. ]', input_text)
    x = ""
    for value in r:
        if any(char.isdigit() for char in value):
            x = value
    try:
        cantidad = f"{r[r.index(x)]} {r[r.index(x) + 1]}"
        if r[r.index(x) + 1] not in ["gramos", "miligramos", "g", "mg", "grams", "miligrams"]:
            cantidad=None

        new_r = [word for word in r if word != x and word != r[r.index(x) + 1]]
        input_buscado = " ".join(new_r)

    except ValueError:
        cantidad="100 gramos"
        new_r=[word for word in r]
        input_buscado = " ".join(new_r)

    resultado={"Nombre comida":input_buscado, "Cantidad":cantidad}
    return resultado

def evento_buscar_comida(request,input_buscar):
    #
    x=separar_nombre_unidad(input_buscar)
    input_cantidad=x["Cantidad"]
    input_nombre_comida=x["Nombre comida"]

    try:
        resultados=foodlist.objects.filter(Nombre__icontains=input_nombre_comida)
        comida_buscada=resultados.first()
        nombre_comida=comida_buscada.Nombre

        model_headers = [field.name for field in comida_buscada._meta.fields]
        tabla={header: getattr(comida_buscada, header) for header in model_headers}

        tabla.pop("id")
        tabla.pop("Nombre")

        lista_headers=tabla.keys()
        lista_valores=[]
        for valor in tabla.values():
            lista_valores.append(valor)

        new_tabla = dict(zip(lista_headers, lista_valores))

        tabla_copy=new_tabla.copy()
        keys_to_remove = []
        for clave, valor in tabla_copy.items():
            if valor == "nulo":
                keys_to_remove.append(clave)

        for clave in keys_to_remove:
            tabla_copy.pop(clave)

        tabla_final_keys=list(tabla_copy.keys())
        tabla_final_values=list(tabla_copy.values())
        z=convertir_entrada_lista(input_cantidad, tabla_final_values)
        tabla_final=dict(zip(tabla_final_keys,z))

    except AttributeError:
        messages.error(request, "Comida no encontrada.....")
        return redirect('nutricion')

    except Exception:
        messages.error(request, "Algo anda mal.....")
        return redirect('nutricion')

    return render(request, 'nutricion.html', {
        "resultados": resultados,
        "nombre_comida": nombre_comida,
        "input_nombre": input_nombre_comida,
        "input_cantidad": input_cantidad,
        "tabla":tabla_final,
    })
