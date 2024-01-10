from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from utils.generate_code import generate_code
from django.utils import timezone
import datetime
from accounts.models import Address


ORDER_STATUS=(

('Reecieved','Reecieved'),
('Processed','Processed'),
('Shiped','Shiped'),
('Delivered','Delivered')
)


# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(User,related_name='orders_woner',on_delete=models.SET_NULL,null=True)
    status=models.CharField(choices=ORDER_STATUS,max_length=12)
    code=models.CharField(default=generate_code,max_length=8)
    order_time=models.DateTimeField(default=timezone.now)
    delivery_time=models.DateTimeField(null=True,blank=True)
    delivery_address=models.ForeignKey(Address,related_name='delivery_address',on_delete=models.SET_NULL,null=True,blank=True)
    coupon=models.ForeignKey('Coupon',related_name='order_coupon',on_delete=models.SET_NULL,null=True,blank=True)




class OrderDetail(models.Model):
    
    order=models.ForeignKey(Order,related_name='order_detail',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='orderdetail_product',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()



class Coupon(models.Model):
    code=models.CharField(max_length=20)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField()
    quantity=models.IntegerField()
    discount=models.FloatField()
    


    def save(self, *args, **kwargs):
        week=datetime.timedelta(days=7)
        self.end_date=self.start_date + week
        super(Coupon,self).save(*args, **kwargs) 