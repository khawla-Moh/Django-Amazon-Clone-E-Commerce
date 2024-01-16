from django.urls import path
from .views import order_list,checkout,add_to_cart
from .api import OrderListAPI



urlpatterns = [
    path('',order_list),
    path('checkout/',checkout),
    path('add_to_cart',add_to_cart),



    #______________api url_________________
    path('api/<str:username>/orders',OrderListAPI.as_view())    #go to order for this user who orderd 

    ]


