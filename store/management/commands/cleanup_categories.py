from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Cleans up unwanted categories and migrates products'

    def handle(self, *args, **kwargs):
        # Target categories to remove
        targets = ['Phones', 'Mobile', 'Accessories', 'phone', 'mobile', 'accessories']
        
        # New destination for phone-like products
        smartphones, _ = Category.objects.get_or_create(name='Smartphones')
        self.stdout.write(f"Ensure 'Smartphones' category exists.")

        for name in targets:
            cats = Category.objects.filter(name__iexact=name)
            for cat in cats:
                products = Product.objects.filter(category=cat)
                count = products.count()
                if count > 0:
                    self.stdout.write(f"Moving {count} products from '{cat.name}' to 'Smartphones'...")
                    products.update(category=smartphones)
                
                self.stdout.write(self.style.WARNING(f"Deleting category: {cat.name}"))
                cat.delete()
        
        self.stdout.write(self.style.SUCCESS("Cleanup complete."))
