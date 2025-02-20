from store.models import Product,Profile




class Cart():
    def __init__(self,request, *args, **kwargs):
        self.session = request.session
        # get request
        self.request = request
        # current session key
        cart = self.session.get('session_key')

        # set new session if new user
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        # make cart available on all pages

        self.cart = cart
    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        # deal with logged in users.
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))
        
    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True

        # deal with logged in users.
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))
          



    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # get all ids
        products_id = self.cart.keys()
        #use ids to look up products
        products = Product.objects.filter(id__in=products_id)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #get the cart
        ourcart = self.cart
        ourcart[product_id] = product_qty


        self.session.modified = True
        
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))

        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)

        ourcart = self.cart
        if product_id in ourcart:
            del ourcart[product_id]

        self.session.modified = True
            
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart = str(carty))

        thing = self.cart
        return thing
    
    def total(self):
        mycart = self.cart
        total = 0
        for v in mycart:
            product = Product.objects.get(id=v)
            if product.is_sale:
                total = total + ( product.sale_price  * mycart[v])
            else:
                total = total + ( product.price  * mycart[v])
        
        return total