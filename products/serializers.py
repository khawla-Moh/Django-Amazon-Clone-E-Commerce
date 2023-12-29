from rest_framework import serializers
from .models import Product,Brand,Reviews,ProductImages



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:

        model=ProductImages
        fields=['image']



class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:

        model=Reviews
        fields=['user','rate','date','review']


class ProductListSerializer(serializers.ModelSerializer):
    brand=serializers.StringRelatedField()
    """  review_count=serializers.SerializerMethodField(method_name='get_review_count')
    avg_rate=serializers.SerializerMethodField()
    """ 
    class Meta:
        model=Product
        fields='__all__'
    
    """
    def get_review_count(self,object):
        reviews=object.review_count()
        return reviews
  
    def get_avg_rate(self,object):
        avg=object.avg_rate()
        return avg
    """
   


class ProductDetailSerializer(serializers.ModelSerializer):
    brand=serializers.StringRelatedField()
    """ review_count=serializers.SerializerMethodField(method_name='get_review_count')
    avg_rate=serializers.SerializerMethodField()
    """
    images=ProductImageSerializer(source='product_images',many=True)
    reviews=ProductReviewSerializer(source='reviews_product',many=True)
    class Meta:
        model=Product
        fields='__all__'
""" 
    def get_review_count(self,object):
        reviews=object.review_count()
        return reviews
 
    def get_avg_rate(self,object):
        avg=object.avg_rate()
                 
        return avg    
 """

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'
