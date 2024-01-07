from django.db import models
from django.contrib.auth.models import User
from products.models import Product

ORDER_STATE=(
('Reecieved','Reecieved'),
('Processed','Processed'),
('Shiped','Shiped')
('Delivered','Delivered')
)


# Create your models here.

class Orders(models.Model):
    user=models.ForeignKey(User,related_name='orders_woner',on_delet=models.SET_NULL,null=True)
    state=models.CharField(choices=ORDER_STATE,max_length=12)
    product=models.ForeignKey(Product,related_name='orders_product',on_delete=models.SET_NULL,null=True)





class OrderDetail(models.Model):
    pass