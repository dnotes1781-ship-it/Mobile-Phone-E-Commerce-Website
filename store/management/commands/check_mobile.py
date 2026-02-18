from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Checks mobile data'

    def handle(self, *args, **kwargs):
        # Find a phone (usually in a category that is not Accessories)
        # Or just search for a known phone name
        mobile = Product.objects.filter(name__icontains='iPhone').first() 
        if not mobile:
             mobile = Product.objects.filter(name__icontains='Samsung').first()
        
        if mobile:
            self.stdout.write(f"Product: {mobile.name}")
            self.stdout.write(f"RAM: '{mobile.ram}' (Truthiness: {bool(mobile.ram)})")
            self.stdout.write(f"Storage: '{mobile.storage}'")
            self.stdout.write(f"Camera: '{mobile.camera}'")
        else:
            self.stdout.write("No mobile found to check.")
