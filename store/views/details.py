from django.shortcuts import render, get_object_or_404
from store.models.product import Product

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    
    # Fetch variants group (Self + Parent + Siblings)
    variant_group = []
    if product.parent:
        variant_group = list(product.parent.variants.all()) + [product.parent]
    else:
        # Include self if it has variants
        if product.variants.exists():
            variant_group = list(product.variants.all()) + [product]

    color_options = []
    storage_options = []

    if variant_group:
        # Get unique values
        all_colors = set(p.color for p in variant_group if p.color)
        all_storages = set(p.storage for p in variant_group if p.storage)
        
        # Build Color Buttons
        for c in all_colors:
            # Find best match: Same Color + Current Storage
            match = next((p for p in variant_group if p.color == c and p.storage == product.storage), None)
            # Fallback: Just Same Color
            if not match:
                match = next((p for p in variant_group if p.color == c), None)
            
            if match:
                color_options.append({
                    'name': c,
                    'id': match.id,
                    'active': c == product.color
                })

        # Build Storage Buttons
        for s in all_storages:
            # Find best match: Same Storage + Current Color
            match = next((p for p in variant_group if p.storage == s and p.color == product.color), None)
            # Fallback: Just Same Storage
            if not match:
                match = next((p for p in variant_group if p.storage == s), None)
            
            if match:
                storage_options.append({
                    'name': s,
                    'id': match.id,
                    'active': s == product.storage
                })
        
        # Sort
        color_options.sort(key=lambda x: x['name'])
        storage_options.sort(key=lambda x: x['name'])

    # Existing Logic
    similar_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    
    context = {
        'product': product,
        'color_options': color_options,
        'storage_options': storage_options,
        'similar_products': similar_products,
    }
    return render(request, 'detail.html', context)
