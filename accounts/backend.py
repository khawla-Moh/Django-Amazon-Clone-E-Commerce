from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameLogin(ModelBackend):
    def authenticate(self,request,username:None,password: None,**kwargs):
        try:
            user=User.objects.get(email=username)