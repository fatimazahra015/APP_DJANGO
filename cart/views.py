from django.shortcuts import render, get_object_or_404
from .cart import Cart
from Ecommerce_Website.models import produit
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def cart_summary(request):
    # Get the cart 
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    # Combine all context into a single dictionary
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
    }
    return render(request, "cart_summary.html", context)



def cart_add(request):
    # Get the cart 
    cart = Cart(request)
    # Test for POST
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # lookup product in DB 
        product = get_object_or_404(produit, id=product_id)

        #save to session
        cart.add(product=product, quantity=product_qty)

        # Get cart quantity
        cart_quantity = cart.__len__()

        # response =JsonResponse({'Product Name :': product.name  })
        response =JsonResponse({'qty': cart_quantity })
        messages.success(request, ("Product Added To Cart..."))
        return response
        


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))

        # Call delete Function Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        messages.success(request, ("Your Choice Has Been Successfully Deleted "))
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Your Cart Has Been Updated.."))
        return response
        # return redirect('cart_summary')