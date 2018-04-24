from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import NiceThing
from .forms import NiceThingForm, ReportNiceThingForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import mail_admins

def index(request):
    # get a random quote
    nice_thing = NiceThing.objects.filter(reported=False)
    if nice_thing:
        nice_thing = nice_thing.order_by('?').first()

    return render(request, 
                template_name="main/index.html",
                context={'nice_thing': nice_thing})

def thing(request, nice_thing_id):
    nice_thing = get_object_or_404(NiceThing, id=nice_thing_id)

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
    nice_thing = get_object_or_404(NiceThing, id=nice_thing_id)

    if request.method == 'POST':
        form = ReportNiceThingForm(request.POST, instance=nice_thing)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.reported = True
            instance.reported_at = timezone.now()
            instance.save()
            messages.info(request, 
                          'NiceThing reported and will be reviewed. Thank you.')
            mail_admins(
                subject="NiceThing ({}) reported".format(nice_thing_id),
                message="NiceThing {} reported at {}".format(nice_thing_id, 
                                                             instance.reported_at)
            ) 
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ReportNiceThingForm(instance=nice_thing)
        
    return render(request, template_name='main/report.html',
                  context={'form': form})