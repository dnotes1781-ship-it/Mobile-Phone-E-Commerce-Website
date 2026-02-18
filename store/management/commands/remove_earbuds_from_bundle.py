from django.core.management.base import BaseCommand
from store.models.product import Product

class Command(BaseCommand):
    help = 'Removes Earbuds from iPhone 13 Bundle'

    def handle(self, *args, **kwargs):
        iphone = Product.objects.filter(name='iPhone 13').first()
        if not iphone:
            self.stdout.write(self.style.ERROR('iPhone 13 not found.'))
            return

        # Find Earbuds - try generic naming or specific name
        earbuds = Product.objects.filter(name__icontains='Buds').first()
        
        if earbuds:
            if earbuds in iphone.compatible_accessories.all():
                iphone.compatible_accessories.remove(earbuds)
                self.stdout.write(self.style.SUCCESS(f'Removed "{earbuds.name}" from iPhone 13 bundle.'))
            else:
                self.stdout.write(self.style.WARNING(f'"{earbuds.name}" was not in the bundle.'))
        else:
            self.stdout.write(self.style.ERROR('Earbuds not found.'))
