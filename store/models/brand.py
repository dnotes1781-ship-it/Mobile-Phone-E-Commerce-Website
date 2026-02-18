from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_brands():
        return Brand.objects.all()

    def __str__(self):
        return self.name
