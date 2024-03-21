from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# Create your views here.
#from .models import Project, Task
from .models import Producto
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask, CreateNewProject



def hello(request, username):
    print(username)
    return HttpResponse("hello %s " % username)

def about(request):
    return render(request,"about.html")

def projects(request):
    #projects=list(Project.objects.values())
    projects=Project.objects.all()
    return render(request,"projects.html", {
        "projects":projects
    })
def tasks(request):
    #task=get_object_or_404(Task,id=id)
    tasks=Task.objects.all()
    return render(request,"tasks.html",{
        "tasks":tasks
    })
    
def create_task(request):
    if request.method=="GET":
         return render(request,"create_task.html",{
        "form":CreateNewTask()
        })
    else: 
        Task.objects.create(title=request.POST["title"], description=request.POST["description"], project_id=2)
        return redirect("tasks")
   
    
def create_project(request):
    if request.method=="GET":
        return render(request, "create_projects.html",{"form":CreateNewProject})
    else: 
       
        Project.objects.create(name=request.POST["name"])
        return redirect("projects")
        
        #return render(request, "create_projects.html",{"form":CreateNewProject})
        
        
        
        
def index(request):
    productos = Producto.objects.all()
    return render(request,"index.html",{"productos":productos})


def vender(request):
    productos = Producto.objects.all()
    return render(request, "vender.html", {'productos': productos})

def facturas(request):
    return render(request, "facturas.html")

def tickets(request):
    return render(request, "tickets.html")

def devoluciones(request):
    return render(request, "devoluciones.html")
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


   


