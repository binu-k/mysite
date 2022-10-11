
from django.urls import path,include

from .views import index,image



urlpatterns = [
    
    path('',index,name='index page'),
    path('image/',image,name='image'),
]
