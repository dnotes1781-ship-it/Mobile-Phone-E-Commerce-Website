from django.core.management.base import BaseCommand
from store.models.product import Product
from store.models.category import Category

class Command(BaseCommand):
    help = 'Reseeds Accessories with new AI images and detailed specifications'

    def handle(self, *args, **kwargs):
        # 1. Define Categories
        cat_mobile, _ = Category.objects.get_or_create(name='Mobile')
        cat_cover, _ = Category.objects.get_or_create(name='Mobile Phone Cover')
        cat_earbuds, _ = Category.objects.get_or_create(name='Earbuds')
        cat_charger, _ = Category.objects.get_or_create(name='Charger')
        cat_protector, _ = Category.objects.get_or_create(name='Screen Protector')

        # 2. Clear Old Accessories (by specific names or categories to be safe)
        # We will delete all products in these accessory categories to ensure a fresh start
        Product.objects.filter(category__in=[cat_cover, cat_earbuds, cat_charger, cat_protector]).delete()
        self.stdout.write(self.style.WARNING("Deleted old accessories."))

        # 3. Create New Products

        # -- Phone Cover --
        cover = Product.objects.create(
            name='Luxury Silicone/TPU Case',
            price=2499,
            category=cat_cover,
            description='Premium dual-layered silicone case with microfiber lining.',
            image='uploads/products/iphone_case_blue.png',
            specifications={
                "Material": "Silicone/TPU (Flexible, shock-absorbing, soft-touch)",
                "Design Type": "Back Cover with MagSafe support",
                "Functional Features": "Drop Protection (10ft), Raised Bezels for Screen/Camera",
                "Compatibility & Fit": "Precision-molded for iPhone 13 / 14 Series",
                "Color": "Midnight Blue"
            }
        )
        self.stdout.write(f"Created {cover.name}")

        # -- Earbuds --
        earbuds = Product.objects.create(
            name='Pro Sound Wireless Buds',
            price=4999,
            category=cat_earbuds,
            description='Active Noise Cancelling wireless earbuds with deep bass.',
            image='uploads/products/wireless_earbuds_white.png',
            specifications={
                "Battery Life": "8h buds / 40h total with case. Fast charging supported.",
                "Audio Quality": "11mm Dynamic Drivers, 20Hz-20kHz Frequency Response",
                "Noise Cancellation": "45dB Hybrid ANC with Transparency Mode",
                "Connectivity": "Bluetooth 5.4, Multipoint Connection, Google Fast Pair",
                "IP Rating": "IP55 Water & Dust Resistant",
                "Controls": "Touch controls for Volume, Playback, and ANC"
            }
        )
        self.stdout.write(f"Created {earbuds.name}")

        # -- Charger --
        charger = Product.objects.create(
            name='20W Fast Power Adapter',
            price=1499,
            category=cat_charger,
            description='Compact USB-C PD charger for rapid charging.',
            image='uploads/products/usb_charger_adapter.png',
            specifications={
                "Voltage (V)": "5V / 9V (Auto-switching)",
                "Amperage (A)": "3A Max",
                "Wattage (W)": "20W Power Delivery (PD 3.0)",
                "USB PD / QC": "Supports PD 3.0 and QC 4.0+",
                "Safety Certifications": "UL, CE, RoHS, FCC Certified",
                "Built-in Safety": "Over-heat, Over-current, Short-circuit protection",
                "Input": "100-240V AC, 50/60Hz (Global Voltage)"
            }
        )
        self.stdout.write(f"Created {charger.name}")

        # -- Screen Protector --
        glass = Product.objects.create(
            name='9H Tempered Glass',
            price=799,
            category=cat_protector,
            description='Ultra-clear, scratch-resistant screen protection.',
            image='uploads/products/screen_protector_glass.png',
            specifications={
                "Hardness": "9H (Diamond-level scratch resistance)",
                "Thickness": "0.33mm ultra-thin design",
                "Transparency": "99.9% High Transparency (Crystal Clear)",
                "Impact Protection": "Reinforced edges, shatter-proof layer",
                "Application": "Bubble-free installation kit included",
                "Special Coatings": "Oleophobic (Anti-fingerprint) & Hydrophobic"
            }
        )
        self.stdout.write(f"Created {glass.name}")

        # 4. Update iPhone 13 Specs (User mentioned "in mobile it should have...")
        iphone = Product.objects.filter(name='iPhone 13').first()
        if iphone:
            iphone.specifications = {
                "Processor (CPU)": "A15 Bionic (6-core CPU, 4-core GPU, 16-core Neural Engine)",
                "RAM": "4GB LPDDR4X",
                "Storage": "128GB NVMe",
                "Display": "6.1 Super Retina XDR OLED, HDR10, Dolby Vision, 1200 nits peak",
                "Battery Life": "3227mAh, MagSafe & Qi Wireless Charging, 20W Fast Charging",
                "Camera System": "Dual 12MP (Wide f/1.6, Ultra-wide f/2.4), Sensor-shift OIS",
                "Connectivity": "5G Sub-6GHz, Wi-Fi 6 (802.11ax), Bluetooth 5.0, NFC",
                "Build Quality": "Corning-made Glass front/back, Aerospace-grade Aluminum frame, IP68",
                "Operating System": "Upgradable to latest iOS"
            }
            iphone.save()

            # 5. Link for Bundle
            # Clear old and add new
            iphone.compatible_accessories.clear()
            iphone.compatible_accessories.add(cover, earbuds, charger, glass)
            iphone.save()
            self.stdout.write(self.style.SUCCESS('Updated iPhone 13 specs and linked new accessories.'))
        else:
             self.stdout.write(self.style.ERROR('iPhone 13 not found to link accessories. please seed it first.'))

