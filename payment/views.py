from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from Ecommerce_Website.models import produit,Profile
import datetime



def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the orders 
        orders = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == 'true':
                orders = Order.objects.filter(id=pk) 
                now = datetime.datetime.now()
                orders.update(shipped=True,date_shipped=now)

            else:
                orders = Order.objects.filter(id=pk)
                orders.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('base')

        return render(request, 'orders.html',{'orders':orders,'items':items})
    else:
        messages.success(request, "Access Denied !!")
        return redirect('base')



def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            # grab Date and Time
            now = datetime.datetime.now()
            # update orders
            order.update(shipped=True,date_shipped=now)
            # redirect 
            messages.success(request, "Shipping Status Updated")
            return redirect('base')
        return render(request, 'not_shipped_dash.html',{'orders':orders})
    else:
        messages.success(request, "Access Denied !!")
        return redirect('base')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            # grab Date and Time
            now = datetime.datetime.now()
            # update orders
            order.update(shipped=False)
            # redirect 
            messages.success(request, "Shipping Status Updated")
            return redirect('base')
        return render(request, 'shipped_dash.html',{'orders':orders})
    else:
        messages.success(request, "Access Denied !!")
        return redirect('base')



def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']   

        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        if request.user.is_authenticated:
            # logged in 
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items 
            # Get the Order ID 
            order_id = create_order.pk

            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Fetch the product instance
                product_instance = produit.objects.get(id=product_id)
                
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
            
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            produit=product_instance,  # Use the product instance
                            user=user,
                            quantity=value,
                            price=price
                        )
                        create_order_item.save()
                        
            # Delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Order Placed!")
            return redirect('base')

        else:
            # not logged in
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Add order items 
            # Get the Order ID 
            order_id = create_order.pk

            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Fetch the product instance
                product_instance = produit.objects.get(id=product_id)
                
                # Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
            
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(
                            order_id=order_id,
                            produit=product_instance,  # Use the product instance
                            quantity=value,
                            price=price
                        )
                        create_order_item.save()

            # Delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                
            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")
                    

            messages.success(request, "Order Placed!")
            return redirect('base')
    else:
        messages.success(request, "Access Denied")
        return redirect('base')







def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check to see if user is logged in
        if request.user.is_authenticated:
            # Get the Billing Form
            billing_form = PaymentForm()
            return render(request, 'billing_info.html',{'cart_products': cart_products,'quantities': quantities,'totals': totals,'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            # Not Logged in
            # Get the Billing Form        
            return render(request, 'billing_info.html',{'cart_products': cart_products,'quantities': quantities,'totals': totals,'shipping_info': request.POST, 'billing_form': billing_form})



        shipping_form = request.POST
        return render(request, 'billing_info.html',{'cart_products': cart_products,'quantities': quantities,'totals': totals,'shipping_form': shipping_form})

    else:
        messages.success(request, "Access Denied")
        return redirect('base')
    
    

def checkout(request):
    # Get the cart 
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as logged in user
        shipping_user, created = ShippingAddress.objects.get_or_create(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)

    # Combine all context into a single dictionary after defining shipping_form
    context = {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form,  # Add it here after it's defined
    }

    return render(request, 'checkout.html', context)

def payment_success(request):
    return render(request, 'payment_success.html', {})
