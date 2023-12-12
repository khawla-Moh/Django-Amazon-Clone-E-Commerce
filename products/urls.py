from django.urls import path
from .views import ProductList,ProductDetail,BrandList,BrandDetails




urlpatterns = [
     path('brands',BrandList.as_view()),
     path('brands/<slug:slug>',BrandDetails.as_view()),
     path('',ProductList.as_view()),
     path('<slug:slug>',ProductDetail.as_view()),
]