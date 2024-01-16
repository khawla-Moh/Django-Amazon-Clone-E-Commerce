from rest_framework import serializers
from .models import Cart,CartDetail,Order,OrderDetail


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartDetail
        field='__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_detail=CartDetailSerializer(many=True)
    class Meta:
        model=Cart
        field='__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartDetail
        field='__all__'


class OrderSerializer(serializers.ModelSerializer):
    
    order_detail=OrderDetailSerializer(many=True)
    class Meta:
        model=Cart
        field='__all__'
                