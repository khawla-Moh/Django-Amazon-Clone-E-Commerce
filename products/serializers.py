from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from .models import Product,Brand,Reviews,ProductImages



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:

        model=ProductImages
        fields=['image']



class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:

        model=Reviews
        fields=['user','rate','date','review']


class ProductListSerializer(serializers.ModelSerializer,TaggitSerializer,):

    brand=serializers.StringRelatedField()
    tags = TagListSerializerField()
    """ 
    #to make avg_rate and count_review showed in product detail api
    review_count=serializers.IntegerField()
    avg_rate=serializers.FloatField()
    """
    
    """  review_count=serializers.SerializerMethodField(method_name='get_review_count')
    avg_rate=serializers.SerializerMethodField()
    """ 
    class Meta:
        model=Product
        fields=['name','flag','price','sku','subtitle','description','brand','review_count','avg_rate','tags']
    
    """
    def get_review_count(self,object):
        reviews=object.review_count()
        return reviews
  
    def get_avg_rate(self,object):
        avg=object.avg_rate()
        return avg
    """
   


class ProductDetailSerializer(serializers.ModelSerializer,TaggitSerializer):
    brand=serializers.StringRelatedField()
    tags = TagListSerializerField()
    images=ProductImageSerializer(source='product_images',many=True)
    reviews=ProductReviewSerializer(source='reviews_product',many=True)
   
    """ 
    def get_review_count(self,object):
        reviews=object.review_count()
        return reviews
 
    def get_avg_rate(self,object):
        avg=object.avg_rate()
                 
        return avg    
    """

    """ 
    *****************************************************************************
    review_count=serializers.SerializerMethodField(method_name='get_review_count')
    avg_rate=serializers.SerializerMethodField()
    *****************************************************************************
    """
    """
    *****************************************************************************
    #to make avg_rate and count_review showed in product detail api
    review_count=serializers.IntegerField()
    avg_rate=serializers.FloatField()
    *****************************************************************************
    """
    
    """ 
    ********************************************************************************
        def get_review_count(self,object):
            reviews=object.review_count()
            return reviews
    
        def get_avg_rate(self,object):
            avg=object.avg_rate()
                    
            return avg    
    **********************************************************************************        
    """
    class Meta:
   
        model=Product
        fields=['name','flag','price','sku','subtitle','description','brand','review_count','avg_rate','tags','images','reviews']




  
class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'
