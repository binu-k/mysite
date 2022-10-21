
from django.urls import path,include

from .views import index,product,product_details



urlpatterns = [
    
    path('',index,name='index page'),
    path('product/',product,name='product'),
    path('product/<int:id>',product_details,name='product_details'),

]
