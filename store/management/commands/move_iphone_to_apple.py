from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Moves iPhone 13 to Apple category and removes iPhones category'

    def handle(self, *args, **kwargs):
        # 1. Create/Get Apple Category
        apple_cat, created = Category.objects.get_or_create(name='Apple')
        if created:
            self.stdout.write(self.style.SUCCESS('Created "Apple" category.'))

        # 2. Find iPhone 13 and Update
        iphone = Product.objects.filter(name='iPhone 13').first()
        if iphone:
            iphone.category = apple_cat
            iphone.save()
            self.stdout.write(self.style.SUCCESS(f'Moved "{iphone.name}" to "Apple" category.'))
        else:
            self.stdout.write(self.style.WARNING('iPhone 13 not found.'))

        # 3. Delete iPhones Category
        try:
            old_cat = Category.objects.get(name='iPhones')
            # Check if empty or if we want to move all products?
            # User said "remove iphone category and add iphone 13 to apple".
            # I'll check if there are other products.
            others = Product.objects.filter(category=old_cat).exclude(id=iphone.id if iphone else -1)
            if others.exists():
                 self.stdout.write(f"Moving {others.count()} other products from 'iPhones' to 'Apple'...")
                 others.update(category=apple_cat)
            
            old_cat.delete()
            self.stdout.write(self.style.SUCCESS('Deleted "iPhones" category.'))
        except Category.DoesNotExist:
             self.stdout.write('Category "iPhones" did not exist.')
