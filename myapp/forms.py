from django import forms

class CreateNewTask(forms.Form):
    title=forms.CharField(label="Titulo tarea:")
    description=forms.CharField(label="Descripcion de tarea:", widget=forms.Textarea)
    
class CreateNewProject(forms.Form):
    name=forms.CharField(label="name projecttt")

