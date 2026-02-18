from django.core.management.base import BaseCommand
from store.models.product import Product

class Command(BaseCommand):
    help = 'Updates specifications for accessories'

    def handle(self, *args, **kwargs):
        # 1. Update Charger
        charger = Product.objects.filter(name='20W USB-C Fast Charger').first()
        if charger:
            charger.battery = '20W Fast Charge'  # Using 'Battery' field for Power info
            charger.ram = None # Clear N/A
            charger.storage = None
            charger.camera = None
            charger.screen_size = None
            charger.save()
            self.stdout.write(self.style.SUCCESS('Updated Charger specs'))

        # 2. Update Earbuds
        earbuds = Product.objects.filter(name='True Wireless Earbuds').first()
        if earbuds:
            earbuds.battery = '24h Total Playtime'
            earbuds.ram = None
            earbuds.storage = None
            earbuds.camera = None
            earbuds.screen_size = None
            earbuds.save()
            self.stdout.write(self.style.SUCCESS('Updated Earbuds specs'))

        # 3. Update Case
        case = Product.objects.filter(name='Durable Phone Case (iPhone/Android)').first()
        if case:
            # Case doesn't fit well in Battery/RAM. We'll leave them empty to hide the headers.
            # Maybe use Brand (already there)
            case.ram = None
            case.storage = None
            case.camera = None
            case.battery = None
            case.screen_size = '6.1" Compatible' # Using screen size for fit
            case.save()
            self.stdout.write(self.style.SUCCESS('Updated Case specs'))

        # 4. Update Glass
        glass = Product.objects.filter(name='Tempered Glass Screen Protector').first()
        if glass:
            glass.ram = None
            glass.storage = None
            glass.camera = None
            glass.battery = None
            glass.screen_size = '9H Hardness' # Re-purposing Screen Size for Hardness/Type
            glass.save()
            self.stdout.write(self.style.SUCCESS('Updated Glass specs'))
