from rest_framework import generics
from rest_framework.response import Response


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

import datetime

from .serializer import CartDetailSerializer,CartSerializer,OrderSerializer,OrderDetailSerializer
from .models import Cart,CartDetail,Order,OrderDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee


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
        coupon=get_object_or_404(Coupon,code=code)           #from model coupon check if code =code in model or show 404
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
        return ({'message':'coupon not found'})
                

    

