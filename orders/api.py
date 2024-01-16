from rest_framework import generics
from rest_framework.response import Response

from django.contrib.auth.models import User

from .serializer import CartDetailSerializer,CartSerializer,OrderSerializer,OrderDetailSerializer
from .models import Cart,CartDetail,Order,OrderDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee


class OrderListAPI(generics.ListAPIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    """ 

    def get_queryset(self): # this method to override the querty above#
        queryet=super(OrderListAPI,self).get_queryset()
        
        user=User.objects.get(username=self.kwargs['username'])          #kwargs['username'] --> indicate to path ('api/<str:username>/orders
        queryet=queryet.filter(user=user)
        return queryet
    """    
    def list(self,request,*args,**kwargs):                                       #to ovveride the method django provide name list to can ovveride not get_queryset
        queryet=super(OrderListAPI,self).get_queryset()
        
        user=User.objects.get(username=self.kwargs['username'])          
        queryet=queryet.filter(user=user)

        data=OrderSerializer(queryet,many=True).data
        return Response({'orders':data})
