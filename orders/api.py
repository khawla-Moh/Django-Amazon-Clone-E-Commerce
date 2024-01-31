from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import datetime

from .serializer import CartDetailSerializer,CartSerializer,OrderSerializer,OrderDetailSerializer
from .models import Cart,CartDetail,Order,OrderDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee
from accounts.models import Address


class OrderListAPI(generics.ListAPIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()

     

    def get_queryset(self): # this method to override the querty above#
        queryet=super(OrderListAPI,self).get_queryset()
        
        user=User.objects.get(username=self.kwargs['username'])#kwargs['username'] --> indicate to path ('api/<str:username>/orders
        queryet=queryet.filter(user=user)
        return queryet
        
    """
    def list(self,request,*args,**kwargs):    #to ovveride the method django provide name list to can ovveride not get_queryset
        queryet=super(OrderListAPI,self).get_queryset()
        
        user=User.objects.get(username=self.kwargs['username'])          
        queryet=queryet.filter(user=user)

        data=OrderSerializer(queryet,many=True).data
        return Response({'orders':data})
    """



class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()


class ApplyCouponAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user=User.objects.get(username=self.kwargs['username'])          
        coupon=get_object_or_404(Coupon,code=request.data['coupon_code'])           #from model coupon check if code =code in model or show 404
        delivery_fee=DeliveryFee.objects.last().fee
        cart=Cart.objects.get(user=user,status="Inprogress")

        if coupon and coupon.quantity >0:
            tody_date=datetime.datetime.today().date()
            if tody_date >= coupon.start_date and tody_date<= coupon.end_date:
                coupon_value=round( cart.cart_total / 100*coupon.discount,2)         
                subTotal=round( cart.cart_total - coupon_value,2    )
                

                cart.coupon=coupon                                #assign coupon value to cart.coupon field   
                cart.total_with_coupn=subTotal
                cart.save()
                
                coupon.quantity -=1
                coupon.save()

                return Response({'message':'coupon was applied successfuly'})
            else:
                return Response({'message':'coupon was not applied '})
        return Response ({'message':'coupon not found'},status=status.HTTP_200_OK)
                

class CreatetOrderAPI(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        user=User.objects.get(username=self.kwargs['username'])
        code=request.data['payment_code']
        address=request.data['address_id']

        cart=Cart.objects.get(usrt=user,status='Inprogress')
        cart_detail=CartDetail.objects.filter(cart=cart)
        user_address=Address.objects.get(id=address)

        #fill order from cart | order_detail from cart_detail
        new_order=Order.objects.create(
          user=user,
          status= 'Reecieved',
          code=code,
          delivery_address=user_address,
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
        #send email
        return Response({'message':'order was created successfuly'},status=status.HTTP_201_CREATED)         


class CartCreateUpdateDelete(generics.GenericAPIView):
    def get(self,request,*args,**kwargs):  #to get or create a cart
        user=User.objects.get(username=self.kwargs['username'])
        cart,create=Cart.objects.get_or_create(user=user,status='Inprogress')
        data=CartSerializer(cart).data             #cartserialzer contain cartdetail
        return Response({"cart":data})


    def post(self,request,*args,**kwargs): #to add & update
        user=User.objects.get(username=self.kwargs['username'])
        product=Product.objects.get(id=request.data['product_id'])
        quantity=int(request.data['quantity'])
        
        cart=Cart.objects.get(user=user,status='Inprogress')
        cart_detail,created=CartDetail.objects.get_or_create(cart=cart,product=product)           #field cart,product in cartDetial model
        
        cart_detail.quantity=quantity
        cart_detail.total=round(product.price * cart_detail.quantity,2)
        cart_detail.save()
        return Response({'message':'cart was updated successfully'},status=status.HTTP_200_OK)

    
    def delete(self,request,*args,**kwargs):#to delete
        user=User.objects.get(username=self.kwargs['username'])
        product=CartDetail.objects.get(id=request.data['item_id'])
        product.delete()
        return Response({'message':'item was deleted successfully'},status=status.HTTP_202_ACCEPTED)