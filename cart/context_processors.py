from .cart import Cart
from store.models import Category,WishList

# create context processor

def cart(request):

    return {'cart':Cart(request),}

def category(request):
    category = Category.objects.all()

    return {'category':category}

def wishlist(request):
    try:
        wishlist = WishList.objects.get(customer=request.user)
        num_wishlist = wishlist.products.count()
        return {'num_wishlist':num_wishlist}
    except:
        return {}