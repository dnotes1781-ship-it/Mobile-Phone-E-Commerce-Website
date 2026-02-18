from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Product
from store.models.category import Category
from django.views import View
from django.db.models import Min, Max


from django.contrib import messages

# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                        messages.warning(request, "Product removed from cart.")
                    else:
                        cart[product]  = quantity-1
                        messages.warning(request, "Quantity updated.")
                else:
                    cart[product]  = quantity+1
                    messages.success(request, "Product added to cart!")
            else:
                cart[product] = 1
                messages.success(request, "Product added to cart!")
        else:
            cart = {}
            cart[product] = 1
            messages.success(request, "Product added to cart!")

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect(request.META.get('HTTP_REFERER', 'homepage'))



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = Product.objects.all()
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    query = request.GET.get('q')
    
    # 1. Category Filter
    if categoryID:
        products = products.filter(category=categoryID)
    
    # 2. Search Filter
    if query:
        products = products.filter(name__icontains=query)

    # 3. Price Filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Calculate Global Min/Max for Slider
    price_stats = Product.objects.aggregate(Min('price'), Max('price'))
    data = {}
    data['products'] = products
    data['categories'] = categories
    data['min_price_limit'] = price_stats['price__min'] or 0
    data['max_price_limit'] = price_stats['price__max'] or 100000

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)


