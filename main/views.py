from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import NiceThing
from .forms import NiceThingForm

def index(request):
    # get a random quote
    nice_thing = NiceThing.objects.order_by('?').first()

    return render(request, 
                template_name="main/index.html",
                context={'nice_thing': nice_thing})

def add(request):
    if request.method == "POST":
        form = NiceThingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NiceThingForm()

    return render(request, template_name='main/add.html',
                  context={'form': form})

def report(request):
    return HttpResponseRedirect(reverse('index'))