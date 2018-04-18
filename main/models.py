from django.db import models

class NiceThing(models.Model):

    date_added = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    reported = models.BooleanField(default=False)
    reported_at = models.DateTimeField(blank=True, null=True)

    # Reporting inappropriate posts 
    #
    # If a NiceThing has a reported value of True then we need to 
    # look at the content. This will be a seperate app to review
    # reported posts with a DELETE and OK buttons. The reported_at date
    # can be used to prioritise reviewing.

    def __str__(self):
        return "{} - [ {:.40} ]".format(self.date_added.strftime("%d-%m-%Y"), self.text)