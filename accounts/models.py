from django.db import models
from django.contrib.auth.models import User
from utils.generate_code import generate_code
# Create your models here.


class Profile(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile')
    code=models.CharField(max_length=10,defualt=generate_code)

    def __str__(self):
        return str(self.user)



PHONE_TYPE=(
    ('Primary','Primary'),
    ('Secondary','Secondary'),
    
)

class ContactNumbers(models.Model):
    user=models.ForeignKey(User,related_name='user_adddress',on_delete=models.CASCADE)
    type=models.CharField(max_length=10,choices=PHONE_TYPE)
    number=models.CharField(max_length=25)



ADDRESS_TYPE=(
    ('Home','Home'),
    ('Office','Office'),
    ('Bussines','Bussines'),
    ('Other','Other')
)

class Address(models.Model):
    user=models.ForeignKey(User,related_name='address_user',on_delete=models.CASCADE)
    address=models.TextField(max_length=200)
    type=models.CharField(max_length=8,choices=ADDRESS_TYPE) 










