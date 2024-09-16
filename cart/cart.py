from Ecommerce_Website.models import produit, Profile


class Cart():
    def __init__(self,request):
        self.session = request.session

        # Get request
        self.request = request
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # if  the user is n ew , no session key ! Create One!ç
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site 
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = { 'price': str(product.price)}
            self.cart[product_id] = int(product_qty) 

        self.session.modified = True

        # Deak with logged in user 
        if self.request.user.is_authenticated:
            # Get the currnent user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\" ")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))



    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = { 'price': str(product.price)}
            self.cart[product_id] = int(product_qty) 

        self.session.modified = True

        # Deak with logged in user 
        if self.request.user.is_authenticated:
            # Get the currnent user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\" ")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))



    def cart_total(self):
        # Get Products IDS
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = produit.objects.filter(id__in=product_ids)
        # Get Quantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total


    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # get ids from cart
        products_ids = self.cart.keys()


        # Use ids to lookup products in database model
        products = produit.objects.filter(id__in=products_ids)

        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart

        # update Dictionnary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            # Get the currnent user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\" ")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing
    

    def delete(self,product):
        product_id = str(product)
        # Delete from Dictionnary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            # Get the currnent user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\" ")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

        

