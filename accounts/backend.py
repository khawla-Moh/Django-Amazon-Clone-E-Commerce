from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameLogin(ModelBackend):
    
    def authenticate(self, request, username=None, password=None,**kwargs):
    
        try:
            user=User.objects.get(email=username)                #check email
        except User.DoesNotExist: 
            try:
                user=User.objects.get(username=username)         #check username if email not found
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        
        return None    
            
