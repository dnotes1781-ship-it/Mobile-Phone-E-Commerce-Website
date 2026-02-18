import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eshop.settings')
django.setup()

from store.models.category import Category
from store.models.product import Product

def organize_accessories():
    # 1. Get or Create "Accessories" Category
    category_name = "Accessories"
    try:
        category = Category.objects.get(name__iexact=category_name)
        print(f"Found existing category '{category.name}' with ID: {category.id}")
    except Category.DoesNotExist:
        category = Category(name=category_name)
        category.save()
        print(f"Created new category '{category.name}' with ID: {category.id}")

    # 2. Define Keywords for Accessories
    keywords = [
        "charger", "adapter", "usb", "cable",
        "case", "cover", "pouch",
        "protector", "glass", "guard",
        "earbuds", "headphone", "headset", "earphone", "ods", "pods",
        "watch", "band"
    ]

    # 3. Find and Update Products
    count = 0
    all_products = Product.objects.all()
    
    print(f"\nScanning {all_products.count()} products for accessories...")
    
    for product in all_products:
        p_name_lower = product.name.lower()
        if any(keyword in p_name_lower for keyword in keywords):
            # Check if already in category to avoid redundant updates
            if product.category != category:
                old_cat = product.category.name if product.category else "None"
                product.category = category
                product.save()
                print(f"Moved '[{product.id}] {product.name}' from '{old_cat}' to 'Accessories'")
                count += 1
            else:
                print(f"Skipped '[{product.id}] {product.name}' (already in Accessories)")

    print(f"\nTotal accessories moved: {count}")
    print(f"Final Category ID for Accessories: {category.id}")

if __name__ == '__main__':
    organize_accessories()
