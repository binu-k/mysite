
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Product, Cart, OrderHistory
from users.models import Profile
# Create your views here.

def index(request):
    return render(request, 'index.html')






@login_required
def products(request):
    p = Product.objects.all()

    context = {'products':p}
    return render(request, 'products.html', context = context)


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'



def product_details(request, id):
    p = Product.objects.get(id = id)
    context = {'p':p}
    return render(request, 'product_details.html', context = context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'p'



@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        seller = request.user   

        p = Product(name=name, price=price, description=desc, image=image, seller=seller)
        p.save()

        return redirect('products')
    
    return render(request, 'add_product.html')


class ProductCreateView(CreateView):
    model = Product
    fields = ['name','price','description','image','seller']
    template_name = 'add_product.html'
    success_url = reverse_lazy('products')







def update_product(request,id):
    p = Product.objects.get(id = id)
    context = {'p':p}

    if request.method == 'POST':
        p.name = request.POST.get('name')
        p.price = request.POST.get('price')
        p.description = request.POST.get('desc')

        try:
            p.image = request.FILES['upload']
        except Exception as e:
            print(e)
            pass

        p.save()

        return redirect('products')
    
    return render(request, 'update_product.html', context = context)



class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name','price','description','image','seller']
    template_name = 'update_product.html'
    context_object_name = 'p'
    success_url = reverse_lazy('products')








def delete_product(request,id):
    p = Product.objects.get(id = id)
    context = {'p':p}

    if request.method == 'POST':
        p.delete()
        return redirect('products')
    
    return render(request, 'delete_product.html', context = context)


class ProductDelete(DeleteView):
    model = Product
    template_name = 'delete_product.html'
    context_object_name = 'p'
    success_url = reverse_lazy('products')






@login_required
def cart_view(request):
# To view the items in the cart

    current_user = request.user
# To get cart items of current user
    cart_items = Cart.objects.filter(user_id = current_user)
# To make a list of product class objects containing products in the cart of current user
    product_object_list = []
    for item in cart_items:
        product_object_list.append(Product.objects.get(id = item.product_id))
# To find the total cart items and update on profile table of current user
    total_cart_items = len(product_object_list)
    profile_object = Profile.objects.get(user_id = current_user)
    profile_object.total_cart_items = total_cart_items
    profile_object.save()

    context = {
        "products": product_object_list,
        }
# To find the input quantity by the current user for each item in the cart
    if request.method == "POST":
        for cart_item in cart_items:
            qty = request.POST.get(str(cart_item.product_id))
            c_obj = Cart.objects.get(product_id = cart_item.product_id, user_id = current_user)
            c_obj.quantity = qty
            c_obj.save()
            
        return redirect('order_summary')
    
    return render(request, 'cart_details.html', context=context)




@login_required
def cart_add(request, id):
# To add items to the cart table
    current_user = request.user
# To avoid adding of similar items in the cart
    cart_item = Cart.objects.filter(user_id = current_user)
    flag = True
    for item in cart_item:
        if int(item.product_id) != id:
            flag = True
        else:
            flag = False
            break

    if flag:        
        p = Product.objects.get(id = id)

        product_id = p.id
        product_name = p.name
        current_user = current_user

        c_add = Cart(product_id = product_id, product_name = product_name, user = current_user)
        c_add.save()

    return redirect('cart_view')






def cart_remove(request, id):
# To remove induvitual items from cart    
    current_user = request.user
    c = Cart.objects.filter(product_id = id, user_id = current_user)
    c.delete()

    return redirect('cart_view')




def order_summary(request):
# To view oder summary
    current_user = request.user

    cart_items = Cart.objects.filter(user_id = current_user)

    product_object_list = []
    for cart_item in cart_items:
        product_object_list.append(Product.objects.get(id = cart_item.product_id))
# To find total amount based on the quantity and price
    total_amount = 0
    for product_item in product_object_list:
        for cart_item in cart_items:
            if product_item.id == cart_item.product_id:
                total_amount = total_amount + (product_item.price * cart_item.quantity)

    context = {
        "products": product_object_list,
        "cart" : cart_items,
        "total_amount" : total_amount
        }

    return render(request, "order_summary.html", context=context)



def payment_success(request):
# To perfome after payment     
    current_user = request.user
    cart_items = Cart.objects.filter(user_id = current_user)
# To write odered items to oderhistory table
    for item in cart_items:
        oder_object = OrderHistory() 
        oder_object.product_id = item.product_id
        oder_object.product_name = item.product_name
        oder_object.user = current_user
        oder_object.quantity = item.quantity
        oder_object.save()
# after writing oderhistory table, deleteing all cart items of current user        
    cart_items.delete()

    profile_object = Profile.objects.get(user_id = current_user)
    profile_object.total_cart_items = 0
    profile_object.save()

    return render(request, "payment_success.html")




def order_history(request):
# To view orderd items of current user
    current_user = request.user
    oder_items = OrderHistory.objects.filter(user_id = current_user)

    product_object_list = []
    for item in oder_items:
        product_object_list.append(Product.objects.get(id = item.product_id))
    
    context = {
        "products" : product_object_list,
        "oder_items" : oder_items
        }

    return render(request, "order_history.html", context = context)

















