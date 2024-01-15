from .models import Cart,CartDetail


def get_cart_data(request):
    if request.user.is_authenticated:
        cart,ceated=Cart.objects.get_or_create(user=request.user,status='Inprogress')
        cart_details=CartDetail.objects.filter(cart=cart)
        return {'cart_data':cart,'cart_details_data':cart_details}
    else:
        return {}
