from django.db import models
from django.contrib.auth.models import User
# Create your models here.



ADDRESS_TYPE=(
    ('Home','Home'),
    ('Office','Office'),
    ('Bussines','Bussines'),
    ('Other','Other')
)

class Address(models.Model):
    user=models.ForeignKey(User,related_name='address_user',on_delet=models.CASCADE)
    address=models.TextField(max_length=200)
