from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Restores iPhone 13, renames Cover, and setups Bundle'

    def handle(self, *args, **kwargs):
        # 1. Rename Cover
        # Search for the one created in reseed_accessories
        cover = Product.objects.filter(name__icontains='Luxury Silicone').first() or \
                Product.objects.filter(name__icontains='Silicone').first()
        
        if cover:
            cover.name = 'iPhone 13 Cover'
            cover.save()
            self.stdout.write(self.style.SUCCESS('Renamed cover to "iPhone 13 Cover"'))
        else:
            self.stdout.write(self.style.WARNING('Cover not found. Creating new one.'))
            cat_cover, _ = Category.objects.get_or_create(name='Mobile Phone Cover')
            cover = Product.objects.create(
                name='iPhone 13 Cover',
                price=2499,
                category=cat_cover,
                image='uploads/products/iphone_case_blue.png',
                description='Premium dual-layered silicone case.'
            )

        # 2. Restore iPhone 13
        # Valid category that isn't "Mobile" or "Phones" since user hated those
        cat_iphone, _ = Category.objects.get_or_create(name='iPhones')
        
        iphone, created = Product.objects.get_or_create(
            name='iPhone 13',
            defaults={
                'price': 69999,
                'category': cat_iphone,
                'description': 'Super bright Super Retina XDR display.',
                'image': 'uploads/products/iphone13.jpg', # Assuming this image still exists or we need to regenerate/copy?
                # I'll check if I have an image. The old seed had 'uploads/products/iphone13.jpg'.
                # Use that for now.
                'specifications': {
                    "Processor (CPU)": "A15 Bionic",
                    "RAM": "4GB",
                    "Storage": "128GB",
                    "Display": "6.1-inch OLED",
                    "Connectivity": "5G, Wi-Fi 6",
                    "Operating System": "iOS 15"
                }
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Restored iPhone 13'))
        else:
            self.stdout.write('iPhone 13 already exists')

        # 3. Link Bundle
        # Get other accessories
        accessories = Product.objects.filter(name__in=['Pro Sound Wireless Buds', '20W Fast Power Adapter', '9H Tempered Glass'])
        
        iphone.compatible_accessories.clear()
        iphone.compatible_accessories.add(cover)
        iphone.compatible_accessories.add(*accessories)
        
        iphone.save()
        self.stdout.write(self.style.SUCCESS(f'Linked {iphone.compatible_accessories.count()} accessories to iPhone 13'))
