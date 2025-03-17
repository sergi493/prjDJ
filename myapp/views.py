from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
# Create your views here.
#from .models import Project, Task
from .models import Producto,Pressupost,ProducteEnPressupost,Pedidos,FacturaCompra,Reparacio, ProducteEnReparacio,Avui
from .models import Persona
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask, CreateNewProject
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from .models import Ticket, ProductoEnTicket, Producto
import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket
from datetime import datetime
from .models import Ticket, ProductoEnTicket, Producto, ProductoEnFactura
from django.utils import timezone
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def hello(request, username):
    print(username)
    return HttpResponse("hello %s " % username)

@login_required
def about(request):
    return render(request,"about.html")

@login_required
def projects(request):
    #projects=list(Project.objects.values())
    projects=Project.objects.all()
    return render(request,"projects.html", {
        "projects":projects
    })
    
@login_required
def tasks(request):
    #task=get_object_or_404(Task,id=id)
    tasks=Task.objects.all()
    return render(request,"tasks.html",{
        "tasks":tasks
    })
    
@login_required
def create_task(request):
    if request.method=="GET":
         return render(request,"create_task.html",{
        "form":CreateNewTask()
        })
    else: 
        Task.objects.create(title=request.POST["title"], description=request.POST["description"], project_id=2)
        return redirect("tasks")
   
@login_required
def create_project(request):
    if request.method=="GET":
        return render(request, "create_projects.html",{"form":CreateNewProject})
    else: 
       
        Project.objects.create(name=request.POST["name"])
        return redirect("projects")
        
        #return render(request, "create_projects.html",{"form":CreateNewProject})
        
        
        
@login_required     
def index(request):
    productos = Producto.objects.all()
    return render(request,"index.html",{"productos":productos})

@login_required
def vender(request):
    productos = Producto.objects.all()
    clientes=Persona.objects.all()

    try:
        ultima_factura = Facturas.objects.latest('id')
    except Facturas.DoesNotExist:
       
        ultima_factura = Facturas(numero=1)

    try:
        
        ultimo_ticket = Ticket.objects.latest('id')
    except Ticket.DoesNotExist:
     
        ultimo_ticket = Ticket(numero=1)
        
    return render(request, "vender.html", {'productos': productos, "clientes": clientes})

@login_required 
def borrar_de_pressupost(request):
    if request.method == "POST":
        data=json.loads(request.body)
        producte=data.get("producte_id")
        pressupost=data.get("pressupost_id")
        #print(producte + pressupost + "qqqwqwqww")
        producte_element=Producto.objects.get(id=producte)
        
        producte_pressupost=ProducteEnPressupost.objects.filter(producte_id=producte_element.id, pressupost_id=pressupost)
        pres=Pressupost.objects.get(id=pressupost)
        for prod in producte_pressupost:
            pres.total-=producte_element.precio*prod.quantitat
            pres.save()
        producte_pressupost.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"}, status=400)

@login_required 
def borrar_de_reparacio(request):
    if request.method == "POST":
        data=json.loads(request.body)
        producte=data.get("producte_id")
        reparacio=data.get("reparacio_id")
        #print(producte + pressupost + "qqqwqwqww")
        producte_element=Producto.objects.get(id=producte)
        
        producte_reparacio=ProducteEnReparacio.objects.filter(producte_id=producte_element.id, reparacio_id=reparacio)
        rep=Reparacio.objects.get(id=reparacio)
        for prod in producte_reparacio:
            rep.total-=producte_element.precio*prod.quantitat
            rep.save()
        producte_reparacio.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"}, status=400)

@login_required
def facturas(request):
    facturas= Facturas.objects.all()
    for factura in facturas:

        nom_cli=Persona.objects.get(id=factura.persona_id).nombre
       
        factura.persona_id=nom_cli
    return render(request, "facturas.html", {"facturas":facturas})



@login_required
def tickets(request):
    tickets = Ticket.objects.all()
    persona=Persona.objects.all()
    numeros_abono = []
    for ticket in tickets:
        if ticket.abono:
            try:
                numero_entero = int(ticket.abono)
                numeros_abono.append(numero_entero)
            except ValueError:
                continue
                
    if request.method == 'POST':
        


        
        for ticket in tickets:
            cantidad_real = request.POST.get('cantidad_real_' + str(ticket.id))
            if cantidad_real:
                print(f"ID del Ticket: {ticket.id}, Cantidad Real: {cantidad_real}")
                ticket.total = cantidad_real
                ticket.save()
                print("Cantidad actualizada")
            else:
                print("No se recibió la cantidad real")

    
    return render(request, "tickets.html", {'tickets': tickets,'persona':persona,'numeros_abono':numeros_abono})




@login_required
def devoluciones(request):
    return render(request, "devoluciones.html")



@login_required
def facturar_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            idTicket=data.get("idTicket")
            idClient=data.get("idClient")
            
            #crear factura amb id client
            ticket = get_object_or_404(Ticket, id=idTicket)
            ultimo_ticket = Ticket.objects.latest('id').id
            ticket.abono=ultimo_ticket +1
            ticket.save()
            productos_en_ticket = ProductoEnTicket.objects.filter(ticket_id=ticket)
            productos_y_cantidades = productos_en_ticket.values('producto', 'cantidad')
            print("aa",productos_en_ticket)
            total = ticket.total
            factura = Facturas.objects.create(
                    date=datetime.now(),
                    total=total,
                    persona_id=idClient,
                    numero=0
            )
            factura.save()
            total=total*(-1)
            ticket = Ticket.objects.create(
                    date=datetime.now(),
                    total=total,
                    abono=idTicket
                    
            )
            ticket.save()
            
            
            ultimo_ticket = Ticket.objects.latest('id')
            
            ultima_factura = Facturas.objects.latest('id')
            
            
            for item in productos_en_ticket:
                cantidad=item.cantidad*(-1)
                Productoenticket= ProductoEnTicket.objects.create(
                    ticket_id=ultimo_ticket,
                    producto_id=item.producto_id,
                    cantidad=cantidad
                )
                Productoenticket.save()
                Productoenfactura=ProductoEnFactura.objects.create(
                    factura_id=ultima_factura,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad
                )
                Productoenfactura.save()
                
                producto = Producto.objects.get(id=item.producto_id)
                producto.cantidad+=int(cantidad)
                print("nnnn",producto.cantidad) 
                producto.save()  
            #en productoenticket poner -1 con referencia al ticket
            #en productoenfactura poner -1 con referencia a la factura
            return JsonResponse({'success': 'Cliente guardado correctamente.'}, status=200)
        except Exception as e:
            print("Error al guardar el ticket:", str(e))  # Add this debug log
            return JsonResponse({'error': 'Error al guardar el ticket.'}, status=500)
   
            
    

def crear_pedido(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            referencia=data.get("referencia")
            quantitat=data.get("quantitat")
            nota=data.get("nota")
            print(referencia)
            producte=Producto.objects.get(codigo=referencia)
            print(producte)
            nou_pedido= Pedidos.objects.create(
                producto_id=producte,
                quantitat=quantitat,
                nota=nota,
               factura_compra="pendent"
               
                
                
            )
            nou_pedido.save()
            
                
            
            return JsonResponse({'success': 'pedido guardado correctamente.'}, status=200)
            
        except Exception as e:
            print("error:", str(e))
            return JsonResponse({'error': 'Error DE METODE.'})
    else:
        return JsonResponse({'error': 'Error DE METODE.'})

def guardar_client_facturar_ticket(request):
   
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nom')  
            dni = data.get('nif')
            direccion= data.get('direccio')
            localitat= data.get("localitat")
            email= data.get('email')
            telefono= data.get('telefon') 
            comp_banc= data.get('banc')
            print(nombre,localitat,dni,direccion,email,telefono,comp_banc)
            cliente = Persona.objects.create(
                    nombre=nombre,
                    nif=dni,
                    localidad=localitat,
                    direccion=direccion,
                    email=email,
                    telefono=telefono,
                    comp_banc=comp_banc
            )
            cliente.save()
            return JsonResponse({'success': 'Cliente guardado correctamente.'}, status=200)
            
        except Exception as e:
            print("Error al guardar el ticket:", str(e))  # Add this debug log
            return JsonResponse({'error': 'Error al guardar el ticket.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
  
    
def crear_nou_pressupost(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clientId = data.get('clientId')  
            total = data.get('total')  
            diccionariProductes = data.get("diccionariProductes")

            print(f"Client ID: {clientId}, Total: {total}")
            print("Productes en pressupost:")
            print(diccionariProductes)

            # Crear l'objecte Pressupost
            pressupost = Pressupost.objects.create(
                persona_id=clientId,
                date=datetime.now(),
                total=total
            )
            pressupost.save()
            # Esperar 2 segons (opcional)
            time.sleep(2)

            # Recuperar l'últim pressupost creat
            pressupost = Pressupost.objects.latest('id').id
            
            # Crear ProducteEnPressupost per a cada element del diccionari
            for referencia, quantitat in diccionariProductes.items():
                
                productos = Producto.objects.filter(codigo=referencia)

                for producto in productos:
                    producteEnpressupost = ProducteEnPressupost.objects.create(
                        pressupost_id=pressupost,  # Utiliza solo el id numérico
                        producte=producto,
                        quantitat=quantitat
                    )
                    producteEnpressupost.save()
                    

                print(f"Producte: {referencia}, Quantitat: {quantitat}")

            return JsonResponse({'success': 'Pressupost creat correctament.'}, status=200)

        except Exception as e:
            print("Error en desar el pressupost:", str(e))
            return JsonResponse({'error': 'Error en desar el pressupost.'}, status=500)

    else:
        return JsonResponse({'error': 'Mètode no permès.'}, status=405)
    
def crear_nou_reparacio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clientId = data.get('clientId')  
            total = data.get('total')  
            diccionariProductes = data.get("diccionariProductes")
            
            print(f"Client ID: {clientId}, Total: {total}")
            print("Productes en pressupost:")
            print(diccionariProductes)

            # Crear l'objecte Pressupost
            reparacio = Reparacio.objects.create(
                persona_id=clientId,
                date=datetime.now(),
                total=total
            )
            reparacio.save()
            # Esperar 2 segons (opcional)
            time.sleep(2)

            # Recuperar l'últim pressupost creat
            reparacio = Reparacio.objects.latest('id').id
            
            # Crear ProducteEnPressupost per a cada element del diccionari
            for referencia, quantitat in diccionariProductes.items():
                
                productos = Producto.objects.filter(codigo=referencia)

                for producto in productos:
                    producteEnreparacio = ProducteEnReparacio.objects.create(
                        reparacio_id=reparacio,  # Utiliza solo el id numérico
                        producte=producto,
                        quantitat=quantitat
                    )
                    producteEnreparacio.save()
                    

                print(f"Producte: {referencia}, Quantitat: {quantitat}")

            return JsonResponse({'success': 'Pressupost creat correctament.'}, status=200)

        except Exception as e:
            print("Error en desar el pressupost:", str(e))
            return JsonResponse({'error': 'Error en desar el pressupost.'}, status=500)

    else:
        return JsonResponse({'error': 'Mètode no permès.'}, status=405)
    
def ultim_client_id(request):
    if request.method == 'GET':  # Usar GET en lugar de POST para obtener datos
            try:
                last_client = Persona.objects.latest('id')
                data = {
                    'id': last_client.id,
                    'nom': last_client.nombre,
                    'telefon': last_client.telefono,
                    'nif': last_client.nif,
                    'email': last_client.email,
                    'localitat': last_client.localidad,
                    'direccio': last_client.direccion,
                    'banc': last_client.comp_banc,
                    }
                return JsonResponse(data)
            except Cliente.DoesNotExist:
                return JsonResponse({'error': 'No clients found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
def aplicar_pressupost(request):
    data=json.loads(request.body)
    id_pressupost=data.get("id_pressupost")
    productes_i_quant=data.get("productes",[])
    print(productes_i_quant,"qqq",id_pressupost)
    total_preu_pressupost=0
    for unitat in productes_i_quant:
            producte_id = unitat.get('producte_id')
            quantitat = unitat.get('quantitat')
            producte_id=Producto.objects.get(codigo=producte_id).id
            producte_preu=Producto.objects.get(id=producte_id).precio
            total_linea=quantitat*producte_preu
            total_preu_pressupost+=total_linea
            
            # Filtrar todas las filas que correspondan al pressupost y producte_id actual
            files = ProducteEnPressupost.objects.filter(pressupost_id=id_pressupost, producte_id=producte_id)
            for fila in files:
                print(f"Actualizando Producte ID: {fila.producte_id}, Cantidad antigua: {fila.quantitat}, Nueva cantidad: {quantitat}")
                fila.quantitat = quantitat  # Actualizar la cantidad
                fila.save()  # Guardar los cambios
    pressupost=Pressupost.objects.get(id=id_pressupost)
    pressupost.total=total_preu_pressupost
    pressupost.save()
    return HttpResponse("aa")
        
    
    

def aplicar_reparacio(request):
    data=json.loads(request.body)
    id_reparacio=data.get("id_reparacio")
    productes_i_quant=data.get("productes",[])
    print(productes_i_quant,"qqq",id_reparacio)
    total_preu_reparacio=0
    for unitat in productes_i_quant:
            print("qq")
            producte_id = unitat.get('producte_id')
            quantitat = unitat.get('quantitat')
            print("ww",producte_id,quantitat)
            producte_id=Producto.objects.get(codigo=producte_id).id
            
            producte_preu=Producto.objects.get(id=producte_id).precio
            total_linea=quantitat*producte_preu
            total_preu_reparacio+=total_linea
            
            # Filtrar todas las filas que correspondan al pressupost y producte_id actual
            files = ProducteEnReparacio.objects.filter(reparacio_id=id_reparacio, producte_id=producte_id)
            for fila in files:
                print(f"Actualizando Producte ID: {fila.producte_id}, Cantidad antigua: {fila.quantitat}, Nueva cantidad: {quantitat}")
                fila.quantitat = quantitat  # Actualizar la cantidad
                fila.save()  # Guardar los cambios
    reparacio=Reparacio.objects.get(id=id_reparacio)
    reparacio.total=total_preu_reparacio
    reparacio.save()
    return HttpResponse("aa")
        
    
    
def afegir_producte_pressupost(request):
    data=json.loads(request.body)
    id_pressupost=data.get("idPressupost")
    id_producte=data.get("id_producte")
    print(id_pressupost)
    nou_producte_en_pressupost=ProducteEnPressupost.objects.create(
        quantitat=1,
        producte_id=int(id_producte),
        pressupost_id=int(id_pressupost)
    )
    pressupost=Pressupost.objects.get(id=id_pressupost)
    producte=Producto.objects.get(id=id_producte)
    pressupost.total+=producte.precio
    pressupost.save()
    return HttpResponse("lllll")


    
def afegir_producte_reparacio(request):
    data=json.loads(request.body)
    id_reparacio=data.get("idReparacio")
    id_producte=data.get("id_producte")
    print(id_reparacio)
    nou_producte_en_reparacio=ProducteEnReparacio.objects.create(
        quantitat=1,
        producte_id=int(id_producte),
        reparacio_id=int(id_reparacio)
    )
    reparacio=Reparacio.objects.get(id=id_reparacio)
    producte=Producto.objects.get(id=id_producte)
    reparacio.total+=producte.precio
    reparacio.save()
    return HttpResponse("lllll")



def guardar_cliente(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            nombre = data.get('nom')  
            dni = data.get('nif')
            direccion= data.get('direccio')
            localitat= data.get("localitat")
            email= data.get('email')
            telefono= data.get('telefon') 
            comp_banc= data.get('banc')
            print(nombre,localitat,dni,direccion,email,telefono,comp_banc)
            cliente = Persona.objects.create(
                    nombre=nombre,
                    nif=dni,
                    localidad=localitat,
                    direccion=direccion,
                    email=email,
                    telefono=telefono,
                    comp_banc=comp_banc
            )
            cliente.save()
            return JsonResponse({'success': 'Cliente guardado correctamente.'}, status=200)
            
        except Exception as e:
            print("Error al guardar el ticket:", str(e))  # Add this debug log
            return JsonResponse({'error': 'Error al guardar el ticket.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)


def guardar_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total = data.get('total')  # Use .get() method to safely retrieve the total
            pagament=data.get("pagament")
            print(pagament)
            print("Total recibido:", total)  # Add this debug log
            if total is not None:  # Check if total is not None before proceeding
                # Create a new entry in the database
                ticket = Ticket.objects.create(
                    date=datetime.now(),
                    total=total,
                    metodo_pago=pagament
                )
                ticket.save()
                return JsonResponse({'message': 'Ticket guardado correctamente.'})
            else:
                return JsonResponse({'error': 'El valor total no fue recibido.'}, status=400)
        except Exception as e:
            print("Error al guardar el ticket:", str(e))  # Add this debug log
            return JsonResponse({'error': 'Error al guardar el ticket.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def guardar_factura(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            total = data.get('totalText')  # Use .get() method to safely retrieve the total
            num_Cli=data.get("num_Cli")
            
            print("Número de cliente recibido:", num_Cli)
            print("Total recibido:", total)  # Add this debug log
            if total is not None:  # Check if total is not None before proceeding
                # Create a new entry in the database
                factura = Facturas.objects.create(
                    date=datetime.now(),
                    total=total,
                    persona_id=num_Cli,
                    numero=0
                )
                factura.save()
                return JsonResponse({'message': 'Fac guardado correctamente.'})
            else:
                return JsonResponse({'error': 'El valor total no fue recibido.'}, status=400)
        except Exception as e:
            print("Error al guardar el ticket:", str(e))  # Add this debug log
            return JsonResponse({'error': 'Error al guardar el ticket.'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def reembolsar_ticket(request):
    
    if request.method=="POST":
        data=json.loads(request.body)
        id=data.get("id")
        
        ticket=Ticket.objects.get(id=id)
       
        ticket_base = get_object_or_404(Ticket, id=id)
        ultim_ticket = Ticket.objects.latest('id').id
        ticket_base.abono=ultim_ticket +1
        ticket_base.save()
        reembolso=Ticket.objects.create(
            
            date=datetime.now(),
            total=ticket.total*(-1),
            metodo_pago=ticket.metodo_pago,
            abono=ticket.id
            
        )
        reembolso.save()
        
        productos_en_ticket = ProductoEnTicket.objects.filter(ticket_id=ticket_base)
        
        print("aaa",productos_en_ticket)
        productos_y_cantidades = productos_en_ticket.values('producto', 'cantidad')
        for item in productos_en_ticket:
            cantidad=item.cantidad*(-1)
            Productoenticket= ProductoEnTicket.objects.create(
                    ticket_id=reembolso,
                    producto_id=item.producto_id,
                    cantidad=cantidad
            )
            Productoenticket.save()
            
            producto = Producto.objects.get(id=item.producto_id)
            producto.cantidad+=int(cantidad)
            print("nnnn",producto.cantidad) 
            producto.save()  
        return JsonResponse({'message': 'Fac guardado correctamente.'})
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
def reembolsar_factura(request):
    if request.method=="POST":
        data=json.loads(request.body)
        id=data.get("id")
        
        factura=Facturas.objects.get(id=id)
        print(factura)
        factura_base = get_object_or_404(Facturas, id=id)
        ultima_factura = Facturas.objects.latest('id').id
        factura_base.abono=ultima_factura +1
        factura_base.save()
        reembolso=Facturas.objects.create(
            persona_id=factura.persona_id,
            date=datetime.now(),
            total=factura.total*(-1),
            metodo_pago=factura.metodo_pago,
            abono=factura.id
            
        )
        reembolso.save()
        
        
        productos_en_factura = ProductoEnFactura.objects.filter(factura_id=factura_base)
        
        print("aaa",productos_en_factura)
        productos_y_cantidades = productos_en_factura.values('producto', 'cantidad')
        print("sss",productos_y_cantidades)
        for item in productos_en_factura:
            cantidad=item.cantidad*(-1)
            Productoenfactura= ProductoEnFactura.objects.create(
                    factura_id_id=reembolso.id,
                    producto_id=item.producto_id,
                    cantidad=cantidad
            )
            Productoenfactura.save()
            
            producto = Producto.objects.get(id=item.producto_id)
            producto.cantidad+=int(cantidad)
            print("nnnn",producto.cantidad) 
            producto.save()  
        return JsonResponse({'message': 'Fac guardado correctamente.'})
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
def obtenir_pressupost(request, pressupostId):
    pressupost = Pressupost.objects.get(id=pressupostId)
    
    dades_persona=Persona.objects.get(id=pressupost.persona_id)
    productes_en_Pressupost = ProducteEnPressupost.objects.filter(pressupost=pressupostId)
    
    productes_i_quantitats = [{'id':producto.producte.id, 'producto_id': producto.producte.codigo,'producto_imagen': producto.producte.imagen.url,'preu': producto.producte.precio, 'nombre': producto.producte.nombre, 'cantidad': producto.quantitat} for producto in productes_en_Pressupost]
    data = {
        'id': pressupost.id,
        'date': pressupost.date,
        'total': pressupost.total,
        'productos': productes_i_quantitats,
        "persona_id":pressupost.persona_id,
        "persona_nom":dades_persona.nombre,
        "facturat":pressupost.facturat
        
    }
    print(data)
    return JsonResponse(data)

def obtenir_reparacio(request, reparacioId):
    reparacio = Reparacio.objects.get(id=reparacioId)
    
    dades_persona=Persona.objects.get(id=reparacio.persona_id)
    productes_en_Reparacio = ProducteEnReparacio.objects.filter(reparacio=reparacioId)
    
    productes_i_quantitats = [{'id':producto.producte.id, 'producto_id': producto.producte.codigo,'producto_imagen': producto.producte.imagen.url,'preu': producto.producte.precio, 'nombre': producto.producte.nombre, 'cantidad': producto.quantitat} for producto in productes_en_Reparacio]
    data = {
        'id': reparacio.id,
        'date': reparacio.date,
        'total': reparacio.total,
        'productos': productes_i_quantitats,
        "persona_id":reparacio.persona_id,
        "persona_nom":dades_persona.nombre,
        "facturat":reparacio.facturat
        
    }
    print(data)
    return JsonResponse(data)

def facturar_pressupost(request):
    data=json.loads(request.body)
    id_press=data.get("id") 
    
    pressupost=Pressupost.objects.get(id=id_press)
    
    print("aas",pressupost)
    nova_factura=Facturas.objects.create(
        persona_id=pressupost.persona_id,
        date= datetime.now(),
        total= pressupost.total,
        procedencia="Pressupost",
        taula_id_procedencia=pressupost.id
    )
    nova_factura.save() 
    ultima_factura=Facturas.objects.latest("id").id
    productes_i_quantitats_pressupost=ProducteEnPressupost.objects.filter(pressupost_id=id_press)
    for producte_i_quantitat in productes_i_quantitats_pressupost:
        producte_factura=ProductoEnFactura.objects.create(
            cantidad=producte_i_quantitat.quantitat,   
            producto_id=producte_i_quantitat.producte_id,
            factura_id_id=ultima_factura
        )
    pressupost.facturat=str(ultima_factura)
    pressupost.save()
    
    
    return HttpResponse("jeee")
    
    
def facturar_reparacio(request):
    data=json.loads(request.body)
    id_rep=data.get("id") 
    
    reparacio=Reparacio.objects.get(id=id_rep)
    
    print("aas",reparacio)
    nova_factura=Facturas.objects.create(
        persona_id=reparacio.persona_id,
        date= datetime.now(),
        total= reparacio.total,
        procedencia="Reparacio",
        taula_id_procedencia=reparacio.id
    )
    nova_factura.save() 
    ultima_factura=Facturas.objects.latest("id").id
    productes_i_quantitats_reparacio=ProducteEnReparacio.objects.filter(reparacio_id=id_rep)
    for producte_i_quantitat in productes_i_quantitats_reparacio:
        producte_factura=ProductoEnFactura.objects.create(
            cantidad=producte_i_quantitat.quantitat,   
            producto_id=producte_i_quantitat.producte_id,
            factura_id_id=ultima_factura
        )
    reparacio.facturat=str(ultima_factura)
    reparacio.save()
    
    
    return HttpResponse("jeee")
    
def get_ticket_data(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    productos_en_ticket = ProductoEnTicket.objects.filter(ticket_id=ticket_id)
    
    productos_y_cantidades = [{'producto_id': producto.producto.codigo,'producto_imagen': producto.producto.imagen.url,'preu': producto.producto.precio, 'nombre': producto.producto.nombre, 'cantidad': producto.cantidad} for producto in productos_en_ticket]
    data = {
        'id': ticket.id,
        'date': ticket.date,
        'total': ticket.total,
        'abono':ticket.abono,
        'metodo_pago': ticket.metodo_pago,
        'productos': productos_y_cantidades
        
    }
    print(data)
    return JsonResponse(data)


def aplicar_rebre_factura_compra(request):
    data=json.loads(request.body)
    data=data.get("data")
    print(data)
   
    factura=FacturaCompra.objects.filter(referencia_factura=data["id"])
    for fact in factura:
        fact.estat="integrat"
        fact.save()
   
    productes = list(data.values())[0]
    for producte in productes:
        prod_id=producte["producte_id"]
        quantitat=producte["quantitat"]
        print(data["id"])
        modificar_pedido=Pedidos.objects.get(factura_compra=data["id"])
        modificar_pedido.quantitat=quantitat
        modificar_pedido.save()
        producte_modificat=Producto.objects.get(id=prod_id)
        producte_modificat.quantitat=producte_modificat.cantidad + int(quantitat)
        print("111",quantitat, producte_modificat.quantitat)
        producte_modificat.save()
        print(producte_modificat)
        
        print("wqwqw",producte["producte_id"])
    pedidos=Pedidos.objects.filter(factura_compra=fact.referencia_factura)
    print("aa",pedidos)
    for pedido in pedidos:
        if pedido.rebut=="NO":
            pedido.rebut="SI"
            pedido.save()
            producte=Producto.objects.get(id=pedido.producto_id_id)
            producte.cantidad+=pedido.quantitat
            producte.save()
        else:
            print("producte ja ficat")
    return JsonResponse({'message': 'Productos guardados correctamente'}, status=200)
    
    
def aplicar_factura_compra(request):
    data=json.loads(request.body)
    data=data.get("data")
    print(data)
   
    
   
    productes = list(data.values())[0]
    for producte in productes:
        prod_id=producte["producte_id"]
        quantitat=producte["quantitat"]
        print(data["id"])
        modificar_pedido=Pedidos.objects.get(factura_compra=data["id"])
        modificar_pedido.quantitat=quantitat
        modificar_pedido.save()
        producte_modificat=Producto.objects.get(id=prod_id)
        producte_modificat.quantitat=producte_modificat.cantidad + int(quantitat)
        print("111",quantitat, producte_modificat.quantitat)
        producte_modificat.save()
        print(producte_modificat)
        
        print("wqwqw",producte["producte_id"])
    
    return JsonResponse({'message': 'Productos guardados correctamente'}, status=200)
    
    
def obtenir_factura_compra(request, facturaReferencia):
    factura=FacturaCompra.objects.get(id=facturaReferencia)  
    print(factura)
    pedidos=Pedidos.objects.filter(factura_compra=factura.referencia_factura)
    
    print(pedidos)
    
    productos_y_cantidades = []
    for pedido in pedidos:
        producto = pedido.producto_id
        productos_y_cantidades.append({
                'producto_id': producto.id,
                'producto_imagen': producto.imagen.url,
                'preu_compra': producto.precio,
                'preu_venta': producto.precio,  # Suponiendo que el precio de compra y venta es el mismo
                'nombre': producto.nombre,
                'nota': pedido.nota,
                'cantidad': pedido.quantitat,
                'total':producto.precio*pedido.quantitat,
                
        })
    total_factura = sum(item['total'] for item in productos_y_cantidades)
    data = {
        'id': factura.referencia_factura,
        'date': factura.data,
        'total': total_factura,
        'productos': productos_y_cantidades,
        "estat":factura.estat
        
    }
    print(data)
    return JsonResponse(data) 

def get_factura_data(request, factura_id):
    factura = Facturas.objects.get(id=factura_id)
    productos_en_factura = ProductoEnFactura.objects.filter(factura_id=factura_id)
    persona = Persona.objects.get(id=factura.persona_id)
    persona_nombre = persona.nombre
    persona_tel=persona.telefono

    productos_y_cantidades = [{'producto_id': producto.producto.codigo,'producto_imagen': producto.producto.imagen.url,'preu': producto.producto.precio, 'nombre': producto.producto.nombre, 'cantidad': producto.cantidad} for producto in productos_en_factura]
    
    data = {
        'id': factura.id,
        'date': factura.date,
        'total': factura.total,
        "persona_id": factura.persona_id,
        "persona_nombre":persona_nombre,
        "telefon":persona_tel,
        'metodo_pago': factura.metodo_pago,
        'productos': productos_y_cantidades,
        "abono":factura.abono,
        "procedencia":factura.procedencia,
        "taula_id_procedencia":factura.taula_id_procedencia
    }
    print(data)
    return JsonResponse(data)


def guardar_productos_ticket(request):
    time.sleep(2)
    if request.method == 'POST':
        # Obtener datos enviados desde el cliente
        data = json.loads(request.body)
        productos = data.get('productos', [])
        pagament=data.get("pagament")

        # Obtener el último ticket creado
        ultimo_ticket = Ticket.objects.latest('id')
        
        # Iterar sobre los productos recibidos
        for producto_data in productos:
            codigo = producto_data.get('codigo')
            cantidad = producto_data.get('cantidad')

            # Buscar el producto en la base de datos por su código
            producto = Producto.objects.get(codigo=codigo)
           
            producto.cantidad-=int(cantidad)
            print("nnnn",producto.cantidad) 
            producto.save()  
            # Crear una nueva entrada de ProductoEnTicket
            ProductoEnTicket.objects.create(
                ticket_id=ultimo_ticket,
                producto=producto,
                cantidad=cantidad,
                preu_venut=producto.precio,
                preu_distribuidor=producto.preu_distribuidor,
                
            )

        # Devolver una respuesta JSON exitosa
        return JsonResponse({'message': 'Productos guardados correctamente'}, status=200)

    # Devolver un error si la solicitud no es POST
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def guardar_productos_factura(request):
    time.sleep(2)
    if request.method == 'POST':
        # Obtener datos enviados desde el cliente
        data = json.loads(request.body)
        productos = data.get('productos', [])
        num_cli=data.get("numCli")
        # Obtener el último ticket creado
        ultima_factura = Facturas.objects.latest('id')
        
        # Iterar sobre los productos recibidos
        for producto_data in productos:
            codigo = producto_data.get('codigo')
            cantidad = producto_data.get('cantidad')

            # Buscar el producto en la base de datos por su código
            producto = Producto.objects.get(codigo=codigo)
            producto.cantidad-=int(cantidad)
            print("nnnn",producto.cantidad) 
            producto.save()                     
            # Crear una nueva entrada de ProductoEnTicket
            ProductoEnFactura.objects.create(
                factura_id=ultima_factura,
                producto=producto,
                cantidad=cantidad,
                preu_distribuidor=producto.preu_distribuidor,
                preu_venut=producto.precio
            )

        # Devolver una respuesta JSON exitosa
        return JsonResponse({'message': 'Productos guardados correctamente'}, status=200)

    # Devolver un error si la solicitud no es POST
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def tancar_caixa(request):
    data=json.loads(request.body)
    
    total=data.get("total")
    marge=data.get("marge")
    
    efectiu=data.get("efectiu")
    targeta=data.get("targeta")
    banc=data.get("banc")
    nova_caixa= Avui.objects.create(
        data=datetime.now(),
        calaix=efectiu,
        targeta=targeta,
        ingressat_banc=banc,
        total=total,
        marge=marge,
        
        
     )
    return HttpResponse("caixa tancada :)")
@login_required
def stock(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        for producto in productos:
            cantidad_real = request.POST.get('cantidad_real_' + str(producto.id))
            if cantidad_real:
                print(f"ID: {producto.id}, Cantidad Real: {cantidad_real}")
                producto.cantidad = cantidad_real
                producto.save()
                print("Cantidad actualizada")
            else:
                print("No se recibió la cantidad real")
    
    return render(request, 'stock.html', {'productos': productos})

@login_required
def clientes(request):
    persona = Persona.objects.all()
   
    return render(request, "clientes.html", {'persona': persona})
 

def ficar_factura_pedido(request):
    data=json.loads(request.body)
    factura=data.get("factura")
    total_dist=data.get("totalDistribuidor")
    total_venda=data.get("totalVenda")
    producte_pedido_id=data.get("producteId")
    print(factura,producte_pedido_id)
    
    
    
    pedido_producte=Pedidos.objects.get(id=producte_pedido_id)
    pedido_producte.factura_compra=factura
    pedido_producte.save()
    producte=Producto.objects.get(id=pedido_producte.producto_id_id)
    producte.precio=total_venda
    producte.preu_distribuidor=total_dist
    producte.save()
    
    if not FacturaCompra.objects.filter(referencia_factura=factura).exists():
        # Crear una nueva factura si no existe
        nova_factura_compra = FacturaCompra.objects.create(
            referencia_factura=factura,
            data=datetime.now(),
            total=total_dist
        )
        nova_factura_compra.save()
    else:
        factura_compra = FacturaCompra.objects.get(referencia_factura=factura)
        factura_compra.total+=total_dist
    return HttpResponse("QQ")

@login_required
def pedidos(request):
    producte_pedidos_per_facturar=Pedidos.objects.filter(factura_compra="pendent")
    print(producte_pedidos_per_facturar)
    
    for prod in producte_pedidos_per_facturar:
        producte=Producto.objects.get(id=prod.producto_id_id)
        prod.referencia=producte.codigo
        prod.descripcio=producte.descripcion
        prod.referencia_venda=producte.precio
        
    factures_compra=FacturaCompra.objects.all()
    dia=timezone.now().date()
    print("cccc",dia)
    tickets=Ticket.objects.filter(date__date=dia)
    print("aaa",tickets)
    productes_info=[]
    tickets_info = []
    for ticket in tickets:
        print(ticket)
        productes_en_ticket=ProductoEnTicket.objects.filter(ticket_id=ticket.id)
        productes_info=[]
        print("azerty",productes_en_ticket)
        for producte_en_ticket in productes_en_ticket:
            producto = producte_en_ticket.producto
           
            producte=Producto.objects.get(id=producto.id)
            print("gggg",producte)
            producte_info = {
                "referencia": producte.codigo,
                "quantitat": producte_en_ticket.cantidad,
                "descripcio": producte.descripcion,
                "stock":producte.cantidad,
                
            }
            productes_info.append(producte_info)
            print("qwerty",productes_info)
        ticket_info = {
            "ticket": ticket,
            "productes": productes_info
        }
        tickets_info.append(ticket_info) 
        
    print(tickets_info)
    
    productes_info=[]
    factures_info=[]
    factures=Facturas.objects.filter(date__date=dia)
    for factura in factures:
        
        productes_en_factura=ProductoEnFactura.objects.filter(factura_id=factura.id)
        productes_info=[]
        
        for producte_en_factura in productes_en_factura:
            producto = producte_en_factura.producto
           
            producte=Producto.objects.get(id=producto.id)
            print("gggg",producte)
            producte_info = {
                "referencia": producte.codigo,
                "quantitat": producte_en_factura.cantidad,
                "descripcio": producte.descripcion,
                "stock":producte.cantidad
            }
            productes_info.append(producte_info)
            print("qwerty",productes_info)
        factura_info = {
            "factura": factura,
            "productes": productes_info
        }
        factures_info.append(factura_info) 
        
    print(factures_info)
    print(tickets_info)
    
    return render(request, "pedidos.html", {"producte_pedidos_per_facturar":producte_pedidos_per_facturar, "factures_compra":factures_compra,"ticket":tickets , "factures":factures,
        "producte_pedidos_per_facturar": producte_pedidos_per_facturar,
        "factures_compra": factures_compra,
        "tickets_info": tickets_info,
        "factures_info": factures_info
    })  
    
   

@login_required
def hoy(request):
    avui = datetime.now().date()  # Obtén la fecha de hoy
    factures = Facturas.objects.filter(date__date=avui)  # Filtra las facturas por la fecha actual
    tickets=Ticket.objects.filter(date__date=avui)
    # Imprime para depuración (puedes eliminar esto en producción)
    cost=0
    preu=0
    total=0
    preu_efectiu=0
    preu_targeta=0
    for factura in factures:
        productes_factura = ProductoEnFactura.objects.filter(factura_id=factura.id)
        for producte in productes_factura:
            cost += producte.preu_distribuidor
            preu += producte.preu_venut
            
        if factura.metodo_pago=="Efectivo":
            preu_efectiu+=factura.total
            
        elif factura.metodo_pago=="Targeta":
            preu_targeta+=factura.total
    # Calcula els costos i preus dels tickets
    for ticket in tickets:
        productes_ticket = ProductoEnTicket.objects.filter(ticket_id=ticket.id)
        for producte in productes_ticket:
            cost += producte.preu_distribuidor
            preu += producte.preu_venut
            
        if ticket.metodo_pago=="Efectivo":
            preu_efectiu+=ticket.total
            
        elif ticket.metodo_pago=="Targeta":
            preu_targeta+=ticket.total
            
    if preu != 0:  # Evita divisió per zero
        marge=preu-cost
        marge_benefici = ((preu - cost) / preu) * 100
    else:
        marge = 0
        marge_benefici = 0
    print(factures)
    
    # Renderiza la plantilla pasando las facturas como contexto
    return render(request, "hoy.html", {'factures': factures,'tickets':tickets,'total':total,'marge':marge,'marge_benefici':marge_benefici,'preu_efectiu':preu_efectiu,'preu_targeta':preu_targeta})

@login_required
def presupostos(request):
    
    personas=Persona.objects.all()
    producte=Producto.objects.all()
    pressupostos=Pressupost.objects.all()
    
    for pres in pressupostos:

        nom_cli=Persona.objects.get(id=pres.persona_id).nombre
       
        pres.persona_id=nom_cli
    
    return render(request, "presupostos.html",{"persona":personas,"producte":producte,"pressupostos":pressupostos})

@login_required
def reparacions(request):
    
    personas=Persona.objects.all()
    producte=Producto.objects.all()
    reparacions=Reparacio.objects.all()
    
    for repara in reparacions:

        nom_cli=Persona.objects.get(id=repara.persona_id).nombre
       
        repara.persona_id=nom_cli
    
    return render(request, "reparacions.html",{"persona":personas,"producte":producte,"reparacions":reparacions})

@login_required
def filtrar_tickets(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        inici = data.get('inici')
        fi = data.get('fi')

        # Convertir les dates a un format que Django pugui entendre
        try:
            tickets = Ticket.objects.filter(date__range=[inici, fi])
            tickets_list = list(tickets.values())
            return JsonResponse(tickets_list, safe=False)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


   
@login_required
def afegir_ultim_producte(request):
    time.sleep(1)
    ultim_producte=Producto.objects.latest('id')
    data = {
        "id":ultim_producte.id,
                'nom': ultim_producte.nombre,
                'referencia': ultim_producte.codigo,
                'quantitat': ultim_producte.cantidad,
                'descripcio': ultim_producte.descripcion,
                'preu': ultim_producte.precio
            }
    print(data)
    return JsonResponse(data)
    
    
@login_required
def crear_producte(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            nom = data.get("nom")
            referencia = data.get("referencia")
            quantitat = data.get("quantitat")
            descripcio = data.get("descripcio")
            preu = data.get("preu")
            preu_compra = data.get("preuCompra")
            imatge = data.get("imatge")
            if not imatge:
                imatge="imagenes/configure.png"
            prod= Producto.objects.create(
                    nombre=nom,
                    codigo=referencia,
                    cantidad=quantitat,
                    descripcion=descripcio,
                    precio=preu,
                    imagen=imatge,
                    preu_distribuidor=preu_compra
            )
            resposta = {'id': prod.id}
            return JsonResponse(resposta, status=201)
            
            
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dades JSON no vàlides"}, status=400)
    return render(request, 'stock.html')
 
@login_required
def modificar_client(request):
    
    if request.method=="POST":
        data = json.loads(request.body.decode('utf-8'))
        referencia= data.get("referencia")
        nom= data.get("nom")
        carrer= data.get("carrer")
        localitat= data.get("localitat")
        tel= data.get("tel")
        banc= data.get("banc")
        email= data.get("email")
        nif= data.get("nif")
            
        base_dades_producte = Persona.objects.get(id=referencia)
        
        base_dades_producte.localidad=localitat
        base_dades_producte.calle=carrer
        base_dades_producte.nombre=nom
        base_dades_producte.nif=nif  
        base_dades_producte.telefono=tel 
            
        base_dades_producte.email=email  
            
        base_dades_producte.banc=banc  
        base_dades_producte.save()
            
        return HttpResponse("Producte actualitzat correctament")
      
@login_required
def client_datos(request, clientId):
    try:
         client= Persona.objects.get(id=clientId)
         client_dades={
             "client_id":client.id,
             "client_nom":client.nombre,
             "client_localitat":client.localidad,
             "client_carrer":client.calle,
             "client_nif":client.nif,
             "client_telefon":client.telefono,
             "client_email":client.email,
             "client_comp_banc":client.comp_banc
         }
    
         return JsonResponse(client_dades)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Client no trobat'}, status=404)
@login_required
def producte_datos(request, producteId):
   
    try:
        
        producte = Producto.objects.get(codigo=producteId)
        producte_dades = {
            'producto_id': producte.codigo,
            
            'preu': producte.precio,
            'nombre': producte.nombre,
            'cantidad': producte.cantidad,
            "preu_distribuidor":producte.preu_distribuidor,
            "imatge":producte.imagen.url
        }
        
        if producte.imagen.url:
            producte_dades['imatge'] = producte.imagen.url
            
        return JsonResponse(producte_dades)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
@login_required
def modificar_producte(request):
    if request.method=="POST":
        data = json.loads(request.body)
        producte = data.get('producte')
        referencia = data.get('referencia')
        quantitat = data.get('quantitat')
        preu = data.get('preu')
        preuCompra = data.get('preuCompra')
        nom = data.get('nom')
        print("qqq",producte)
        base_dades_producte = Producto.objects.get(codigo=producte)
        
        base_dades_producte.codigo=referencia
        base_dades_producte.precio=preu
        base_dades_producte.nombre=nom
        base_dades_producte.cantidad=quantitat   
        base_dades_producte.preu_distribuidor=preuCompra  
         
        base_dades_producte.save()
        
        return HttpResponse("Producte actualitzat correctament")
    
@login_required
def estadisticas(request):
    tickets = Ticket.objects.all()
    df = pd.DataFrame(list(tickets.values()))

    metodo_pago_count = df['metodo_pago'].value_counts()
    total_tickets = metodo_pago_count.sum()
    porcentaje_efectivo = (metodo_pago_count.get('Efectiu', 0) / total_tickets) * 100
    porcentaje_tarjeta = (metodo_pago_count.get('Targeta', 0) / total_tickets) * 100
    porcentaje_domiciliacio = (metodo_pago_count.get('Domiciliacio', 0) / total_tickets) * 100
    porcentaje_chec = (metodo_pago_count.get('Chec bancari', 0) / total_tickets) * 100

    plt.figure(figsize=(6,4))
    plt.title('Métodos de Pago')
    sns.set(style="whitegrid")
    colors = sns.color_palette('dark', 4)
    plt.pie(
        [porcentaje_efectivo, porcentaje_tarjeta, porcentaje_domiciliacio, porcentaje_chec],
        labels=['Efectiu', 'Targeta', 'Domiciliacio', 'Chec bancari'],
        autopct='%1.1f%%',
        colors=colors,  # Aplicar los colores personalizados
        startangle=140,
        textprops={'color': 'black'}
        
        
    )
    
    plt.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    
    
    

    data=datetime.now().date()
    print(data)
    principi = datetime.combine(data, datetime.min.time())
    final = datetime.combine(data, datetime.max.time())

# Filtrar facturas y tickets por el rango de fecha actual
    factures = Facturas.objects.filter(date__range=(principi, final))
    tickets = Ticket.objects.filter(date__range=(principi, final))     
    # Sumar el total de todas las facturas del día
    # Sumar el total de todas las facturas y tickets del día
    total_factura = sum(factura.total for factura in factures)
    total_tickets = sum(ticket.total for ticket in tickets)
    print(total_tickets,tickets)
    df = pd.DataFrame(list(factures.values()))
    
    # Contar los métodos de pago
  
    data = {
    'Categoria': ['Factures', 'Tickets'],
    'Total': [total_factura, total_tickets]
    }
    df = pd.DataFrame(data)

    # Create the bar plot
    plt.figure(figsize=(6,4))
    plt.title('Métodos de Pago de Facturas (Hoy)')
    sns.set(style="whitegrid")
    barplot = sns.barplot(x='Categoria', y='Total', data=df, palette='dark')
    
# Annotate bars with the total value at the base
    for p in barplot.patches:
        # Get the height of the bar and the x position
        height = p.get_height()
        x = p.get_x() + p.get_width() / 2.
        # Annotate at the base of the bar (0), slightly offset to avoid overlap
        barplot.annotate(format(height, '.2f'), 
                        (x, 0),  # Position at the base
                        ha='center', va='bottom',
                        xytext=(0, 5),  # Offset to make sure text is visible
                        textcoords='offset points',
                        color='black')
                        
    plt.xlabel('Método de Pago')
    plt.ylabel('Cantidad')
    
    # Guardar la gráfica en un buffer de memoria
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png1 = buffer.getvalue()
    buffer.close()
    
    
    
    
    tickets = Ticket.objects.all().values('date', 'total')
    df = pd.DataFrame(tickets)

    # Asegurarse de que la columna 'date' sea de tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Crear columnas para la fecha y hora
    df['data'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['total'] = df['total'].abs()
    # Sumarizar las ventas por hora
    df['time_slot'] = df['hour'] + (df['minute'] // 30) * 0.5  # Crear franjas horarias de 30 minutos
    hourly_sales = df.groupby(['data', 'time_slot'])['total'].sum().reset_index()

    # Convertir la columna 'data' a su representación ordinal
    hourly_sales['data_ordinal'] = hourly_sales['data'].apply(lambda x: x.toordinal())

    # Entrenar el modelo
    X = hourly_sales[['data_ordinal', 'time_slot']]
    y = hourly_sales['total']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predecir para hoy
    today = datetime.now().date()
    today_ordinal = today.toordinal()
    prediction_times = [
        9.5,  # 9:30 a 10:00
        10.0, # 10:00 a 10:30
        10.5, # 10:30 a 11:00
        11.0, # 11:00 a 11:30
        11.5, # 11:30 a 12:00
        12.0, # 12:00 a 12:30
        12.5, # 12:30 a 13:00
        17.0, # 17:00 a 17:30
        17.5, # 17:30 a 18:00
        18.0, # 18:00 a 18:30
        18.5  # 18:30 a 19:00
    ]
    prediction_data = pd.DataFrame({'data_ordinal': [today_ordinal]*len(prediction_times), 'time_slot': prediction_times})
    predictions = model.predict(prediction_data)

    # Crear un diccionario con las predicciones
    prediction_dict = {
        '9:30 - 10:00': predictions[0],
        '10:00 - 10:30': predictions[1],
        '10:30 - 11:00': predictions[2],
        '11:00 - 11:30': predictions[3],
        '11:30 - 12:00': predictions[4],
        '12:00 - 12:30': predictions[5],
        '12:30 - 13:00': predictions[6],
        '17:00 - 17:30': predictions[7],
        '17:30 - 18:00': predictions[8],
        '18:00 - 18:30': predictions[9],
        '18:30 - 19:00': predictions[10],
    }
    fig, ax = plt.subplots()
    times = list(prediction_dict.keys())
    values = list(prediction_dict.values())

    ax.bar(times, values)
    ax.set_xlabel('Time Slot')
    ax.set_ylabel('Total Tickets')
    ax.set_title('Predicted Ticket Sales')
    plt.xticks(rotation=45, ha='right')  # Rotar los labels para evitar superposición
    plt.subplots_adjust(bottom=0.25)  # Ajustar el margen inferior para dar más espacio

    # Convertir el gráfico a una imagen en formato base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png2 = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png2).decode('utf-8')
    

    # Pasar la imagen codificada a la plantilla
    context = {
        'predictions': image_base64,
        
    }
    
    # Convertir la imagen a base64
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    graphic1 = base64.b64encode(image_png1)
    graphic1 = graphic1.decode('utf-8')
    
    graphic2 = base64.b64encode(image_png2)
    graphic2 = graphic2.decode('utf-8')

    # Incluir la imagen base64 en la plantilla
    context = {'graphic': graphic,'graphic1': graphic1,'predictions': graphic2}
    return render(request, 'estadisticas.html', context)

    





def signup(request):
    if request.method=="GET":
        print("enviant formulari...")
        return render(request, "signup.html",{"form": UserCreationForm})
    else:
        if request.POST["password1"]==request.POST["password2"]:
           
            try:
                user= User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
                user.save()
                login(request,user)
                return redirect("vender")
            except IntegrityError:
                return render(request, "signup.html",{"form": UserCreationForm, "error": "User already exists"})
                
        print(request.POST)
        print("obtenint datos...")
        return render(request, "signup.html",{"form": UserCreationForm, "error": "password do not match"})


from django.shortcuts import render
from .models import Facturas, Ticket

@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "login.html",{"form":  AuthenticationForm})
    else:
        user= authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(request.POST)
        if user is None:
            return render(request, "login.html",{"form":  AuthenticationForm,"error":"User or password is incorrect"}, )
        else:
            login(request,user)
            return redirect("index")
        