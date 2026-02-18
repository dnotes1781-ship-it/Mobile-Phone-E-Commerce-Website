from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Seeds Bundle Data'

    def handle(self, *args, **kwargs):
        # Ensure Categories
        phone_cat, _ = Category.objects.get_or_create(name='Phones')
        acc_cat, _ = Category.objects.get_or_create(name='Accessories')

        # Create iPhone 13
        iphone, created = Product.objects.get_or_create(
            name='iPhone 13',
            defaults={
                'price': 69999,
                'category': phone_cat,
                'description': 'Super bright Super Retina XDR display.',
                'image': 'uploads/products/iphone13.jpg',
                'brand': 'Apple',
                'ram': '4GB',
                'storage': '128GB',
                'color': 'Midnight'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created iPhone 13'))
        else:
            self.stdout.write('iPhone 13 already exists')

        # Create Accessories
        charger, _ = Product.objects.get_or_create(
            name='20W USB-C Power Adapter',
            defaults={
                'price': 1900,
                'category': acc_cat,
                'description': 'Fast charging adapter.',
                'image': 'uploads/products/charger.jpg'
            }
        )

        case, _ = Product.objects.get_or_create(
            name='MagSafe Silicone Case',
            defaults={
                'price': 4900,
                'category': acc_cat,
                'description': 'Silky, soft-touch finish.',
                'image': 'uploads/products/case.jpg'
            }
        )

        glass, _ = Product.objects.get_or_create(
            name='Tempered Glass Protector',
            defaults={
                'price': 999,
                'category': acc_cat,
                'description': '9H Hardness Protection.',
                'image': 'uploads/products/glass.jpg'
            }
        )

        # Link Accessories
        iphone.compatible_accessories.add(charger, case, glass)
        iphone.save()

        self.stdout.write(self.style.SUCCESS(f'Linked accessories to {iphone.name}'))
