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
    review_count=serializers.SerializerMethodField(method_name='get_review_count')
    avg_rate=serializers.SerializerMethodField()
    
    class Meta:
        model=Product
        fields='__all__'
    

    def get_review_count(self,object):
        reviews=object.review_count()
        return reviews
    
    def get_avg_rate(self,object):
        avg=object.avg_rate()
                 
        return avg    



class ProductDetailSerializer(serializers.ModelSerializer):
    brand=serializers.StringRelatedField()
    review_count=serializers.SerializerMethodField(method_name='get_review_count')
    avg_rate=serializers.SerializerMethodField()
    images=ProductImageSerializer(source='product_images',many=True)
    reviews=ProductReviewSerializer(source='reviews_product',many=True)
    class Meta:
        model=Product
        fields='__all__'

    def get_review_count(self,object):
        reviews=object.reviews_product.all().count()
        return reviews
 
    def get_avg_rate(self,object):
        reviews=object.reviews_product.all()
        total=0
        if len(reviews)>0:
            for item in reviews:
                total +=item.rate
            avg=total /len(reviews)    
        else:
            avg=0
                 
        return avg    


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'

class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields='__all__'
