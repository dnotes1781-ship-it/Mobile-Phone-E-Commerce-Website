from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Seeds Dynamic Specification Data'

    def handle(self, *args, **kwargs):
        # define categories
        cat_mobile, _ = Category.objects.get_or_create(name='Mobile')
        cat_cover, _ = Category.objects.get_or_create(name='Mobile Phone Cover')
        cat_earbuds, _ = Category.objects.get_or_create(name='Earbuds')
        cat_charger, _ = Category.objects.get_or_create(name='Charger')
        cat_protector, _ = Category.objects.get_or_create(name='Screen Protector')

        # 1. Mobile (Update iPhone 13 if exists, or create new)
        iphone = Product.objects.filter(name='iPhone 13').first()
        if iphone:
            iphone.specifications = {
                "Processor (CPU)": "A15 Bionic chip",
                "RAM": "4GB",
                "Storage": "128GB (Available: 256GB, 512GB)",
                "Display": "6.1-inch Super Retina XDR OLED",
                "Battery Life": "3227mAh, 20W Fast Charging",
                "Camera System": "12MP Wide + 12MP Ultra Wide with OIS",
                "Connectivity": "5G, Wi-Fi 6, Bluetooth 5.0, NFC",
                "Build Quality": "Ceramic Shield front, Glass back, Aluminum design (IP68)",
                "Operating System": "iOS"
            }
            iphone.save()
            self.stdout.write(self.style.SUCCESS('Updated iPhone 13 Specs'))

        # 2. Cover
        cover, _ = Product.objects.get_or_create(
            name='MagSafe Silicone Case',
            defaults={
                'price': 4900, 'category': cat_cover, 
                'image': 'uploads/products/case.jpg',
                'description': 'Silky, soft-touch finish.'
            }
        )
        cover.specifications = {
            "Material": "Silicone/TPU",
            "Design Type": "Back Cover with MagSafe",
            "Functional Features": "Drop Protection, raised lip for screen/camera",
            "Compatibility & Fit": "iPhone 13 / 13 Pro (Precision Molded)"
        }
        cover.save()
        self.stdout.write(self.style.SUCCESS(f'Updated {cover.name} Specs'))

        # 3. Earbuds
        earbuds, _ = Product.objects.get_or_create(
            name='OnePlus Nord Buds 3',
            defaults={
                'price': 2999, 'category': cat_earbuds,
                'image': 'uploads/products/earbuds.jpg',
                'description': 'Powerful sound with ANC.'
            }
        )
        earbuds.specifications = {
            "Battery Life": "Up to 8h (ANC on) / 12h (off). Case: 28h/43h.",
            "Audio Quality": "12.4mm Driver, 20Hz-20kHz",
            "Noise Cancellation": "Up to 32dB Active Noise Cancellation",
            "Connectivity": "Bluetooth 5.4, Dual Connection Support",
            "Physical Design": "4.2g per earbud, IP55 Dust/Water Resistance",
            "Additional Features": "HeyMelody App, Fast Pair"
        }
        earbuds.save()
        self.stdout.write(self.style.SUCCESS(f'Updated {earbuds.name} Specs'))

        # 4. Charger
        charger, _ = Product.objects.get_or_create(
            name='20W USB-C Power Adapter',
            defaults={
                'price': 1900, 'category': cat_charger,
                'image': 'uploads/products/charger.jpg',
                'description': 'Compact and fast.'
            }
        )
        charger.specifications = {
            "Voltage (V)": "5V/9V",
            "Amperage (A)": "3A/2.22A",
            "Wattage (W)": "20W Max Output",
            "USB PD / QC": "USB Power Delivery 3.0",
            "Input/Output Labels": "100-240V AC, 50/60Hz, USB-C Port",
            "Safety Certifications": "CE, RoHS, UL",
            "Built-in Safety": "Over-current, Short-circuit protection"
        }
        charger.save()
        self.stdout.write(self.style.SUCCESS(f'Updated {charger.name} Specs'))

        # 5. Screen Protector
        glass, _ = Product.objects.get_or_create(
            name='Tempered Glass Protector',
            defaults={
                'price': 999, 'category': cat_protector,
                'image': 'uploads/products/glass.jpg',
                'description': 'Superior protection for your screen.'
            }
        )
        glass.specifications = {
            "Hardness": "9H (Diamond-like hardness)",
            "Thickness": "0.33mm",
            "Transparency": "99% High Clarity",
            "Impact Protection": "IK03 Rated",
            "Scratch Resistance": "Excellent",
            "Application": "Includes Easy Align tray and dust stickers",
            "Special Features": "Anti-fingerprint Oleophobic coating"
        }
        glass.save()
        self.stdout.write(self.style.SUCCESS(f'Updated {glass.name} Specs'))

