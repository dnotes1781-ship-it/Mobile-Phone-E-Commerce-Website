from django.http import JsonResponse
from store.models.product import Product
from store.models.category import Category
from django.views import View

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        # User is typing: Find products starting with query
        # Case insensitive search
        products = Product.objects.filter(name__icontains=query)[:10]
        results = [{'name': p.name, 'id': p.id, 'image': p.image.url} for p in products]
    else:
        # Predefined Searches (could be categories or popular items)
        # For now, let's use Categories and some hardcoded generic terms
        categories = Category.get_all_categories()
        results = [{'name': c.name, 'type': 'Category'} for c in categories]
        results.extend([
            {'name': 'Top Selling Mobiles', 'type': 'Popular'},
            {'name': 'New Arrivals', 'type': 'Popular'}
        ])

    return JsonResponse({'results': results})
