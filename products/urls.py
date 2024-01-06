from django.urls import path
from .views import ProductList,ProductDetail,BrandList,BrandDetails,mydebug,add_review
from . import api





urlpatterns = [
     path('debug',mydebug),
     path('brands',BrandList.as_view()),
     path('brands/<slug:slug>',BrandDetails.as_view()),
     path('',ProductList.as_view()),
     path('<slug:slug>',ProductDetail.as_view()),
     path('<slug:slug>/add-review',add_review),
   



#api url
    path('api/list/',api.ProductListAPI.as_view()),
    path('api/list/<int:pk>',api.ProductDetailAPI.as_view()),
    path('api/brands/',api.BrandListAPI.as_view()),
    path('api/brands/<int:pk>',api.BrandDetailAPI.as_view()),



]