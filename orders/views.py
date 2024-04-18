from django.shortcuts import render,redirect,get_object_or_404
import datetime

from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Order,OrderDetail,Cart,CartDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee
# Create your views here.
def order_list(request):
    data=Order.objects.filter(user=request.user)
    return render(request,'orders/order_list.html',{'orders':data})


def checkout(reguest):
    cart=Cart.objects.get(user=reguest.user,status="Inprogress")
    cart_detail=CartDetail.objects.filter(cart=cart)
    delivery_fee=DeliveryFee.objects.last().fee
   

    #____________________applying Coupon___________________
    if reguest.method=='POST':
        code=reguest.POST['coupon_code']
        #coupon=Coupon.objects.get(code=code)
        coupon=get_object_or_404(Coupon,code=code)           #from model coupon check if code =code in model or show 404
        #_applying Coupon if there is a coupon it isn't expired & it isn't finsh & ___________________
        if coupon and coupon.quantity >0:
            tody_date=datetime.datetime.today().date()
            if tody_date >= coupon.start_date and tody_date<= coupon.end_date:
                coupon_value=round( cart.cart_total / 100*coupon.discount,2)         
                subTotal=round( cart.cart_total - coupon_value,2    )
                total=round( subTotal + delivery_fee,2)
                

                cart.coupon=coupon                                #assign coupon value to cart.coupon field   
                cart.total_with_coupn=subTotal
                cart.save()

                coupon.quantity -=1
                coupon.save()


                return render(reguest,'orders/checkout.html',{
                    "cart_detail":cart_detail,
                    "subTotal":subTotal,
                    "delivery_fee":delivery_fee,
                    "discount":coupon_value,
                    "total":total
                    })

    subTotal=cart.cart_total 
    discount=0
    total=subTotal +delivery_fee
     

    return render(reguest,'orders/checkout.html',{
        "cart_detail":cart_detail,
        "subTotal":subTotal,
        "delivery_fee":delivery_fee,
        "discount":discount,
        "total":total
        })
 

def add_to_cart(request):
   product=Product.objects.get(id=request.POST['product_id'])
   quantity=int(request.POST['quantity'])

   cart=Cart.objects.get(user=request.user,status='Inprogress')
   cart_detail,created=CartDetail.objects.get_or_create(cart=cart,product=product)           #field cart,product in cartDetial model
   cart_detail.quantity=quantity
   cart_detail.total=round(product.price * cart_detail.quantity,2)
   cart_detail.save()
   
   #get new data after create using ajax
   cart=Cart.objects.get(user=request.user,status='Inprogress')
   cart_detail=CartDetail.objects.filter(cart=cart)           #field cart,product in cartDetial model
   
   page=render_to_string('cart_includes.html',{'cart_details_data':cart_detail,'cart_data':cart}) # {% for review in reviews %}
   return JsonResponse({'result':page})
    

   #return redirect(f'/products/{product.slug}')