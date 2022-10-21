from cmath import pi
from multiprocessing import context
from django.shortcuts import render

from .models import Product

def index(request):

    li=['abin','sobin','treesa']
    context={'names':li}
    
    return render(request,'index.html',context=context)


def product(request):

    p=Product.objects.all()
    context={'product':p}

    return render(request,'product.html',context=context)



def product_details(request,id):

    p=Product.objects.get(id=id)
    context={'p':p}


    return render(request,'product_details.html',context=context)
