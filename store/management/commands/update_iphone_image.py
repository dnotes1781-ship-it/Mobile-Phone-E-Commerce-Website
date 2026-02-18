from django.core.management.base import BaseCommand
from store.models.product import Product

class Command(BaseCommand):
    help = 'Updates iPhone 13 image'

    def handle(self, *args, **kwargs):
        iphone = Product.objects.filter(name='iPhone 13').first()
        if iphone:
            iphone.image = 'uploads/products/iphone_13_new.png'
            iphone.save()
            self.stdout.write(self.style.SUCCESS('Updated iPhone 13 image.'))
        else:
            self.stdout.write(self.style.ERROR('iPhone 13 not found.'))
