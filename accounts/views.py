from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profile

from .forms import SignupForm,UserActivateForm

from django.core.mail import send_mail


from products.models import Product,Brand,Reviews  
from orders.models import Order   

# Create your views here.

def signup(request):
      
    """ if request.user.is_authenticated:
        return redirect('/') """ 
    

    if request.method == 'POST':
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
   
    return render(request,'accounts/signup.html',{'form':form})

    '''
      -create new user
      -send email (code activation):code
      -redirct to acitvate page
    '''



def user_activate(request,username):


    
    profile=Profile.objects.get(user__username=username)   
    if request.method=='POST':
        form=UserActivateForm(request.POST)
        if form.is_valid():
           code=form.cleaned_data['code']
           if code== profile.code:
              profile.code=''
           
              user=User.objects.get(username=username)
              user.is_active=True
           
              user.save()
              profile.save()
           
              return redirect('/accounts/login')
           
              

    else:
        form=UserActivateForm()
    
    return render(request,'accounts/activate.html',{'form':form})

    '''
    -recivee code activation
    -redirect to login page
    '''    



def dashboard(request):
    users=User.objects.all().count()
    products=Product.objects.all().count()
    brands=Brand.objects.all().count()
    reviews=Reviews.objects.all().count()
    

    new_products=Product.objects.filter(flag='new')
    sale_products=Product.objects.filter(flag='Sale')
    feature_products=Product.objects.filter(flag='Feature')

    return render(request,'accounts/dashboard.html',
    {
      'users':users,
      'products':products,
      'brands':brands,
      'reviews':reviews,
      'new_products':new_products, 
      'sale_products':sale_products,
      'feature_products':feature_products
    })  