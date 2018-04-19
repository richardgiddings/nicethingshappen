from django.contrib import admin
from .models import NiceThing

class NiceThingAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'reported', 'reported_at', 'shortened_text')
    list_filter = ('reported',)

admin.site.register(NiceThing, NiceThingAdmin)