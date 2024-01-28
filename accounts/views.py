from django.shortcuts import render,redirect
from django.contrib.auth.models import User

from .forms import SignupForm,UserActivateForm

# Create your views here.

def signup(request):
   if request.method=='POST':
    form=SignupForm(request.POST)
    if form.is_valid():
       form.save()                      #triggle signal ---> create profile ---> code 

   else:
    form=SignupForm
   
   return render(request,'account/signup.html',{'form':form})

   '''
      -create new user
      -send email (code activation):code
      -redirct to acitvate page
    '''
def user_activate(request):
    if request.method=='POST':
        form=UserActivateForm(request.POST)

    else:
        form=SignupForm
    
    return render(request,'account/activate.html',{'form':form})

    '''
    -recivee code activation
    -redirect to login page
    '''    