from django.db import  models


class Contactus(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.CharField(max_length=1000)

    def register(self):     # when we do work on live server we have to register table field always.
        self.save()
