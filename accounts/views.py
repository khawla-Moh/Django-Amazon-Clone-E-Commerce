from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profile

from .forms import SignupForm,UserActivateForm

from django.core.mail import send_mail

# Create your views here.

def signup(request):
   if request.method=='POST':
    form=SignupForm(request.POST)
    if form.is_valid():
       username=form.cleaned_data['username']
       email=form.cleaned_data['email']

       user=form.save(commit=False)    
       user.is_active=False                                    #signup(create account but not activates yet)


       form.save()                                             #triggle signal ---> create profile ---> code

       profile=Profile.objects.get(user__username= username)   #get activation code from profile
       #sending email 
       
       send_mail(
            "Activate Your Account",
            f"Welcome {username} \n Use this code {profile.code} to avtivate your account",
            "pythondeveloper6@gmail.com",
            ["email"],
            fail_silently=False,
        ) 
       return redirect(f'/accounts/{username}/activate')



   else:
    form=SignupForm()
   
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