from django.shortcuts import render
from .models import NiceThing

def index(request):
    # get a random quote
    nice_thing = NiceThing.objects.order_by('?').first()

    return render(request, 
                template_name="main/index.html",
                context={'nice_thing': nice_thing})