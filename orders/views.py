from django.shortcuts import render
from .models import Order
# Create your views here.
def ordersData(request):
    data=Order.object.all().ordey_by('price')
    data2=Order.object.all().filter()