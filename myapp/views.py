from multiprocessing import context
from django.shortcuts import render

def index(request):

    li=['abin','sobin','treesa']
    context={'names':li}
    
    return render(request,'index.html',context=context)


def image(request):

   
    
    return render(request,'image.html')



