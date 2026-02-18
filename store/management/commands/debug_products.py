from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'List all products and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write("--- Categories ---")
        for c in Category.objects.all():
            self.stdout.write(f"- {c.id}: {c.name}")
        
        self.stdout.write("\n--- Products ---")
        for p in Product.objects.all():
            self.stdout.write(f"- {p.id}: {p.name} (Category: {p.category.name}) [Image: {p.image}]")
