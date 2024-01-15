from django.shortcuts import render,redirect
from .models import Order,OrderDetail,Cart,CartDetail,Coupon
from products.models import Product
# Create your views here.
def order_list(request):
    data=Order.objects.filter(user=request.user)
    return render(request,'orders/order_list.html',{'orders':data})


def checkout(reguest):
    return render(reguest,'orders/checkout.html',{})


def add_to_cart(request):
   product=Product.objects.get(id=request.POST['product_id'])
   quantity=request.POST['quantity']
   cart=Cart.objects.get(user=request.user,status='Inprogress')
   cart_detail,created=CartDetail.objects.get_or_create(cart=cart,product=product)           #field cart,product in cartDetial model
   
   cart_detail.total=round(product.price * cart_detail.quantity,2)
   cart_detail.save()
   return redirect(f'/products/{product.slug}')