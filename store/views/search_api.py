from django.http import JsonResponse
from store.models.product import Product

def search_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        # Simple name-based search for autocomplete suggestions
        products = Product.objects.filter(name__icontains=query)[:5]
        results = [p.name for p in products]
    else:
        results = []
    return JsonResponse({'results': results})
