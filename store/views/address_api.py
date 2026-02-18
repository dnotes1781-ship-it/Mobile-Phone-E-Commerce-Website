from django.http import JsonResponse

# This view was likely used for the society/address autocomplete feature
def search_societies(request):
    # Returning empty list for now, as the actual data was likely an external API or static list
    return JsonResponse({'results': []})
