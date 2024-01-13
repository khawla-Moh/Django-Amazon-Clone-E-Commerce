from django.shortcuts import render
from .models import Order,OrderDetail,Cart,CartDetail,Coupon
# Create your views here.
def order_list(request):
    data=Order.objects.filter(user=request.user)
    return render(request,'orders/order_list.html',{'orders':data})


def checkout(reguest):
    return render(reguest,'orders/checkout.html',{})


