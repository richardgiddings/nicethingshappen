from django.db import models
from django.template.defaultfilters import truncatechars

class NiceThing(models.Model):

    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=400)

    # Reporting inappropriate posts 
    #
    # If a NiceThing has a reported value of True then we need to look at
    # the content. The reported_at date can be used to prioritise reviewing.

    reported = models.BooleanField(default=False)
    reported_at = models.DateTimeField(blank=True, null=True)
    reported_reason = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "{} - [ {:.40} ]".format(self.date_added.strftime("%d-%m-%Y"), self.text)

    @property
    def shortened_text(self):
        return truncatechars(self.text, 40)