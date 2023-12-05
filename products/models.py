from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone

FLAG_TYPE=(

    ('New','New'),
    ('Sale','Sale'),
    ('Feature','Feature')
)

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length= 150)
    flag=models.CharField(max_length=15,choices=FLAG_TYPE)
    price=models.FloatField()
    image=models.ImageField(upload_to='product')
    sku=models.IntegerField()
    subtitle=models.TextField(max_length=400)
    description=models.TextField(max_length=20000)
    tags = TaggableManager() 
    brand=models.ForeignKey('Brand',related_name='product_prand',on_delete=models.SET_NULL,null=True)

class ProductImages(models.Model):
    Product=models.ForeignKey(Product,related_name='product_images',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='productimages')



class Reviews(models.Model):
    user=models.ForeignKey(User,related_name='reviews_user',on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product,related_name='reviews_product',on_delete=models.CASCADE)
    review=models.TextField(max_length=700)
    date=models.DateTimeField(default=timezone.now)
    rate=models.IntegerField(choices=[(i,i) for i  in range(1,6)])


class Brand(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='brand')


    
class User(models.Model):
    pass
class UserPhone(models.Model):
    pass
class UserAdrees(models.Model):
    pass