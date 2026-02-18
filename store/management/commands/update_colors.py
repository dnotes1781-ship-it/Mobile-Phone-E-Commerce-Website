from django.core.management.base import BaseCommand
from store.models.product import Product

class Command(BaseCommand):
    help = 'Populates color fields'

    def handle(self, *args, **kwargs):
        # Update variants created earlier
        # 1. Parent (iPhone 13 128GB)
        # Note checks for "Standard", likely the parent
        parent = Product.objects.filter(variant_name__icontains="Standard").first()
        if parent:
            parent.color = "Black"
            parent.storage = "128GB"
            parent.save()
            self.stdout.write(f"Updated {parent.name} to Black, 128GB")

        # 2. Variant 256GB Black
        v1 = Product.objects.filter(variant_name__icontains="256GB Black").first()
        if v1:
            v1.color = "Black"
            v1.storage = "256GB"
            v1.save()
            self.stdout.write(f"Updated {v1.name} to Black, 256GB")

        # 3. Variant 128GB Gold
        v2 = Product.objects.filter(variant_name__icontains="128GB Gold").first()
        if v2:
            v2.color = "Gold"
            v2.storage = "128GB"
            v2.save()
            self.stdout.write(f"Updated {v2.name} to Gold, 128GB")
