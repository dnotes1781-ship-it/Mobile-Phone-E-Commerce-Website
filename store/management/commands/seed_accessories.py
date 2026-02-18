from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category
import os

class Command(BaseCommand):
    help = 'Seeds the database with Mobile Accessories'

    def handle(self, *args, **kwargs):
        # 1. Get or Create Category
        category, created = Category.objects.get_or_create(name='Accessories')
        if created:
            self.stdout.write(self.style.SUCCESS('Created category "Accessories"'))
        else:
            self.stdout.write(self.style.SUCCESS('Category "Accessories" already exists'))

        # 2. Define Accessories Data
        accessories = [
            {
                'name': '20W USB-C Fast Charger',
                'price': 1299,
                'description': 'High-speed charging for your iPhone and Android devices. Compact and travel-friendly.',
                'image': 'uploads/products/fast_charger.jpg', # Placeholder path, will use existing static image
                'brand': 'PowerMax',
                'ram': 'N/A',
                'storage': 'N/A',
                'camera': 'N/A',
                'battery': 'N/A',
                'screen_size': 'N/A'
            },
            {
                'name': 'True Wireless Earbuds',
                'price': 2499,
                'description': 'Crystal clear sound with active noise cancellation and 24-hour battery life.',
                'image': 'uploads/products/earbuds.jpg',
                'brand': 'AudioPro',
                'battery': '24 Hours',
                'ram': 'N/A',
                'storage': 'N/A',
                'camera': 'N/A',
                'screen_size': 'N/A'
            },
            {
                'name': 'Durable Phone Case (iPhone/Android)',
                'price': 499,
                'description': 'Military-grade drop protection with a sleek, non-slip grip.',
                'image': 'uploads/products/case.jpg',
                'brand': 'ArmorShield',
                'ram': 'N/A',
                'storage': 'N/A',
                'camera': 'N/A',
                'battery': 'N/A',
                'screen_size': 'N/A'
            },
            {
                'name': 'Tempered Glass Screen Protector',
                'price': 299,
                'description': '9H hardness scratch-resistant glass with oleophobic coating.',
                'image': 'uploads/products/glass.jpg',
                'brand': 'ClearView',
                'ram': 'N/A',
                'storage': 'N/A',
                'camera': 'N/A',
                'battery': 'N/A',
                'screen_size': 'N/A'
            }
        ]

        # 3. Create Products
        for item in accessories:
            # Check if product exists to avoid duplicates
            if not Product.objects.filter(name=item['name']).exists():
                product = Product(
                    name=item['name'],
                    price=item['price'],
                    category=category,
                    description=item['description'],
                    # We will use a default image available in static for now, or just reference 'uploads/products/...'
                    # Since we can't easily upload new files, we'll point to an existing one or specific placeholders
                    # For this demo, let's assume we copy 'static/images/mb3.jpg' to 'uploads/products/' logic or just point to it.
                    # Hack: Pointing to a static image path relative to MEDIA_ROOT if possible, or just string.
                    # Ideally, we should copy a file.
                    image='uploads/products/mb3.jpg', # Reusing an existing image as placeholder
                    brand=item['brand'],
                    ram=item['ram'],
                    storage=item['storage'],
                    camera=item['camera'],
                    battery=item['battery'],
                    screen_size=item['screen_size']
                )
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Created product "{product.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Product "{item["name"]}" already exists'))

