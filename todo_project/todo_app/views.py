from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from.models import task
from.forms import TodoForms
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
# Create your views here.

class TaskListView(ListView):
    model = task
    template_name = 'index.html'
    context_object_name = 'obj1'

class TaskDetailView(DetailView):
    model = task
    template_name = 'detail.html'
    context_object_name = 'obj'

class TaskUpdateView(UpdateView):
    model = task
    template_name = 'update.html'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
class TaskDeleteView(DeleteView):
    model = task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')
def index(request):
    obj1=task.objects.all()
    if request.method=='POST':
        name=request.POST.get('name')
        priority=request.POST.get('priority')
        date=request.POST.get('date')
        t=task(name=name,priority=priority,date=date)
        t.save()
    return render(request,'index.html',{'obj1':obj1})
def delete(request,id):
    if request.method=='POST':
        obj=task.objects.get(id=id)
        obj.delete()
        return redirect('/')
    return render(request,'index.html')
def edit(request, id):
    obj1 = task.objects.get(id=id)

    # Manually set initial data for the form fields
    initial_data = {
        'name': obj1.name,
        'priority': obj1.priority,
        'date': obj1.date,
    }

    form = TodoForms(instance=obj1,initial=initial_data,)
    if request.method == 'POST':
        form = TodoForms(request.POST or None, request.FILES,instance=obj1)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request, 'edit.html', {'obj1': obj1, 'form': form})
