from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Deletes Smartphones category and all its products'

    def handle(self, *args, **kwargs):
        # Target category
        targets = ['Smartphones', 'smartphone', 'SmartPhone']
        
        for name in targets:
            try:
                cat = Category.objects.get(name__iexact=name)
                products = Product.objects.filter(category=cat)
                count = products.count()
                
                if count > 0:
                    self.stdout.write(f"Deleting {count} products from '{cat.name}'...")
                    products.delete()
                
                self.stdout.write(self.style.WARNING(f"Deleting category: {cat.name}"))
                cat.delete()
            except Category.DoesNotExist:
                pass
        
        self.stdout.write(self.style.SUCCESS("Smartphones category and products deleted."))
