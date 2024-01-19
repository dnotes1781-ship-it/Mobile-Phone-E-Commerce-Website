from django.db import  models


class Feedback(models.Model):
   
    email = models.EmailField()
    message = models.CharField(max_length=1000)

    def register(self):
        self.save()
