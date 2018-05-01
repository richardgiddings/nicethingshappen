from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import NiceThing
from .forms import NiceThingForm, ReportNiceThingForm, ContactForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
import django_rq
from .tasks import send_email
from django.conf import settings
from django.template.loader import get_template

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
            instance.reported_at = timezone.localtime(timezone.now())
            instance.save()
            messages.info(request, 
                          'NiceThing reported and will be reviewed. Thank you.')

            # queue emails using redis
            queue = django_rq.get_queue('email')
            subject="NiceThing ({}) reported".format(nice_thing_id),
            message="NiceThing {} reported at {}\n\nText: '{}'\n\nReason: '{}'".format(
                                                             nice_thing_id, 
                                                             instance.reported_at,
                                                             instance.text,
                                                             instance.reported_reason)
            job = queue.enqueue(send_email, subject, message, [settings.DEFAULT_FROM_EMAIL])

            return HttpResponseRedirect(reverse('index'))
    else:
        form = ReportNiceThingForm(instance=nice_thing)
        
    return render(request, template_name='main/report.html',
                  context={'form': form})

def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_email = request.POST.get('contact_email', '')
            message = request.POST.get('message', '')
            send_copy = request.POST.get('send_copy', '')

            template = get_template('contact_template.txt')
            context = {
                'contact_email': contact_email,
                'message': message,
            }
            content = template.render(context)

            # send email to admin
            queue = django_rq.get_queue('email')
            job = queue.enqueue(send_email, 
                                "New contact form submission", 
                                content, 
                                [settings.DEFAULT_FROM_EMAIL])

            # has the user asked for a copy to be sent to them too?
            if send_copy:
                job = queue.enqueue(send_email, 
                                    "Your email to nicethingshappen.co.uk", 
                                    message,
                                    [contact_email])

            messages.info(request, 'Email sent. Thank you.')
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'main/contact.html',
                  context={'form': form_class})