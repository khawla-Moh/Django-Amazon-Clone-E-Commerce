from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from utils.generate_code import generate_code
from django.utils import timezone
from accounts.models import Address


ORDER_STATE=(
('Reecieved','Reecieved'),
('Processed','Processed'),
('Shiped','Shiped')
('Delivered','Delivered')
)


# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(User,related_name='orders_woner',on_delet=models.SET_NULL,null=True)
    state=models.CharField(choices=ORDER_STATE,max_length=12)
    code=models.CharField(defualt=generate_code)
    order_time=models(defualt=timezone.now)
    delivery_time=models(null=True,blank=True)
    delivery_address=models.ForeignKey(Address,related_name='delivery_address',on_delete=models.SET_NULL,null=True,blank=True)





class OrderDetail(models.Model):
    
    order=models.ForeignKey(Order,related_name='order_detail',on_delate=models.CASCADE)
    product=models.ForeignKey(Product,related_name='orderdetail_product',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()
