from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import NiceThing
from .forms import NiceThingForm, ReportNiceThingForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages

def index(request):
    # get a random quote
    nice_thing = NiceThing.objects.order_by('?').first()

    return render(request, 
                template_name="main/index.html",
                context={'nice_thing': nice_thing})

def thing(request, nice_thing_id):
    nice_thing = NiceThing.objects.get(id=nice_thing_id)

    return render(request, 
                template_name="main/thing.html",
                context={'nice_thing': nice_thing})

def add(request):
    if request.method == "POST":
        form = NiceThingForm(request.POST)
        if form.is_valid():
            nice_thing = form.save()
            messages.info(request, 'NiceThing added. Thank you.') 
            return HttpResponseRedirect(reverse('thing', 
                                kwargs={ 'nice_thing_id': nice_thing.id }))
    else:
        form = NiceThingForm()

    return render(request, template_name='main/add.html',
                  context={'form': form})

def report(request, nice_thing_id):
    nice_thing = NiceThing.objects.get(id=nice_thing_id)
    if nice_thing.reported:
        messages.info(request, 'NiceThing already reported.')
        return HttpResponseRedirect(reverse('thing', 
                                kwargs={ 'nice_thing_id': nice_thing.id }))

    if request.method == 'POST':
        form = ReportNiceThingForm(request.POST, instance=nice_thing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.reported = True
            instance.reported_at = timezone.now()
            instance.save()
            messages.info(request, 'NiceThing reported. Thank you.') 
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ReportNiceThingForm(instance=nice_thing)
        
    return render(request, template_name='main/report.html',
                  context={'form': form})