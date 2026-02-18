from django.core.management.base import BaseCommand
from store.models.product import Product

class Command(BaseCommand):
    help = 'Seeds product variants'

    def handle(self, *args, **kwargs):
        # Find a mobile to use as parent
        parent = Product.objects.filter(name__icontains='iphone').first()
        if not parent:
            self.stdout.write(self.style.ERROR('No iPhone found to add variants to.'))
            return

        # 1. Update Parent
        parent.variant_name = "Standard (128GB)"
        parent.save()
        self.stdout.write(f'Updated parent: {parent.name}')

        # 2. Create Variant 1 (Higher Storage)
        v1_name = f"{parent.name} - 256GB"
        if not Product.objects.filter(name=v1_name).exists():
            v1 = Product.objects.create(
                name=v1_name,
                price=parent.price + 10000,
                category=parent.category,
                description=parent.description,
                image=parent.image,
                brand=parent.brand,
                ram=parent.ram,
                storage="256GB", # Diff spec
                camera=parent.camera,
                battery=parent.battery,
                screen_size=parent.screen_size,
                parent=parent,
                variant_name="256GB Black"
            )
            self.stdout.write(self.style.SUCCESS(f'Created variant: {v1.variant_name}'))

        # 3. Create Variant 2 (Different Color)
        v2_name = f"{parent.name} - Gold"
        if not Product.objects.filter(name=v2_name).exists():
            v2 = Product.objects.create(
                name=v2_name,
                price=parent.price, # Same price
                category=parent.category,
                description=parent.description,
                image=parent.image, # Ideally diff image
                brand=parent.brand,
                ram=parent.ram,
                storage=parent.storage,
                camera=parent.camera,
                battery=parent.battery,
                screen_size=parent.screen_size,
                parent=parent,
                variant_name="128GB Gold"
            )
            self.stdout.write(self.style.SUCCESS(f'Created variant: {v2.variant_name}'))
