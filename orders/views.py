from django.shortcuts import render,redirect,get_object_or_404
import datetime

from django.conf import settings

from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Order,OrderDetail,Cart,CartDetail,Coupon
from accounts.models import Address
from products.models import Product
from settings.models import DeliveryFee

from utils.generate_code import generate_code

from django.http import JsonResponse
import stripe
# Create your views here.
def order_list(request):
    data=Order.objects.filter(user=request.user)
    return render(request,'orders/order_list.html',{'orders':data})


def checkout(reguest):
    cart=Cart.objects.get(user=reguest.user,status="Inprogress")
    cart_detail=CartDetail.objects.filter(cart=cart)
    delivery_fee=DeliveryFee.objects.last().fee
   
    
    pub_key=settings.STRIPE_API_KEY_PUBLISHABLE


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
                    "total":total,
                    "pub_key":pub_key
                    })

    subTotal=cart.cart_total 
    discount=0
    total=subTotal +delivery_fee
     

    return render(reguest,'orders/checkout.html',{
        "cart_detail":cart_detail,
        "subTotal":subTotal,
        "delivery_fee":delivery_fee,
        "discount":discount,
        "total":total,
        "pub_key":pub_key
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
   
   total=cart.cart_total
   cart_count=len(cart_detail)

   page=render_to_string('cart_includes.html',{'cart_details_data':cart_detail,'cart_data':cart}) # {% for review in reviews %}
   return JsonResponse({'result':page,'total':total,'cart_count':cart_count})
    

   #return redirect(f'/products/{product.slug}')+








def process_payment(request): #create invoice
       cart=Cart.objects.get(user=request.user,status='Inprogress')
       Delivery_fee=DeliveryFee.objects.last().fee

       if cart.total_with_coupn:
           total=cart.total_with_coupn + Delivery_fee

       else:
           total=cart.total + Delivery_fee   
       
       #GENERATE CODE TO NEW ORDER
       code=generate_code()    

       #django seesion
       request.session['order_code']=code 
       request.session.save()
       #GENERATE INVOICE IN STRIPE
       stripe.api_key= settings.STRIPE_API_KEY_SECRET
       checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data': {
                        'currency':'usd',
                        'product_data':{'name':code},
                        'unit_amount':int(total*100)

                        },
                        'quantity':1
                    
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/orders/checkout/payment/success' + '/success.html',
            cancel_url='http://127.0.0.1:8000/orders/checkout/payment/success' + '/cancel.html',
        )
       return JsonResponse({'session':checkout_session})   

def payment_success(request):
       cart=Cart.objects.get(user=request.user,status='Inprogress')
       cartt_detial=CartDetail.objects.filter(cart=cart)
       payment_Address=Address.objects.last()
       
       code=request.session.get('order_code')

       #cart:order |cart_detail :order_detail
       new_order=Order.objects.create(
            user=request.user,
            status= 'Reecieved',
            code=code,
            delivery_address= payment_Address,
            coupon=cart.coupon,
            total_with_coupn=cart.total_with_coupn,
            total=cart.cart_total
            )
            #creae cart details
       for item in cart_detail  :
                product=Product.objects.get(id=item.product.id) 
                OrderDetail.objects.create(
                Order=new_order,
                product=product,
                quantity=item.quantity,
                price=product.price,
                total=round(item.quantity * product.price,2) 
                )
            #decreasse product quantity 
                product.quantity -=item.quantity
                product.save()
            #close cart
       cart.status='Completed'
       cart.save()
       return render(request,'orders/success.html',{'code':code})

def payment_faild(request):
       return render(request,'orders/faile.html',{})
   