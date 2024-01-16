from rest_framework import generics

from django.contrib.auth.models import User

from .serializer import CartDetailSerializer,CartSerializer,OrderSerializer,OrderDetailSerializer
from .models import Cart,CartDetail,Order,OrderDetail,Coupon
from products.models import Product
from settings.models import DeliveryFee


class OrderListAPI(generics.ListAPIView):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()