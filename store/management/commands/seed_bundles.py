from django.core.management.base import BaseCommand
from store.models.product import Product

class Command(BaseCommand):
    help = 'Seeds bundle links'

    def handle(self, *args, **kwargs):
        # 1. Find Main Product (iPhone)
        iphone = Product.objects.filter(name__icontains='iphone').first()
        if not iphone:
            self.stdout.write(self.style.ERROR("iPhone not found"))
            return

        # 2. Find Accessories
        charger = Product.objects.filter(name__icontains='Charger').first()
        case = Product.objects.filter(name__icontains='Case').first()
        glass = Product.objects.filter(name__icontains='Glass').first()

        accessories = [acc for acc in [charger, case, glass] if acc]

        if not accessories:
            self.stdout.write(self.style.ERROR("No accessories found"))
            return

        # 3. Link them
        iphone.compatible_accessories.set(accessories)
        iphone.save()
        
        # Also link to variants if you want them to have bundles too
        if iphone.variants.exists():
            for v in iphone.variants.all():
                v.compatible_accessories.set(accessories)
                v.save()

        self.stdout.write(self.style.SUCCESS(f"Linked {len(accessories)} accessories to {iphone.name}"))
