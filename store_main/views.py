from django.shortcuts import render, redirect
from . import models
# Create your views here.
def home(request):

    # Получить продукты из базы
    all_products = models.Product.objects.all()

    #получить все названия категорий

    all_categories=models.Category.objects.all()

    # Передать на фронт часть
    context = {'products': all_products, 'categories': all_categories}

    return render(request, 'index.html', context)
# Функция для отображения информацций о конкретном продукте
def about_product(request, pk):
    # Получить конкретный продукт или данные из базы
    current_product = models.Product.objects.get(product_name=pk)

    context = {'product':current_product}

    return render(request,'about.html', context)

    #продукты из конкретной категории
def category_products(request,pk):
    products_from_category = models.Category.objects.get(categoryy_name=pk)

    context = {'products': products_from_category}

    return render(request, 'index.html', context)


#поиск товара
def search_for_product(request):
    product_from_front = request.GET.get('search')
    find_product_from_db = models.Product.objects.filter(product_name__contains=product_from_front)

    context = {'products': find_product_from_db}

    return render(request, 'index.html', context)


def add_product_to_cart(request,pk):
    current_product = models.Product.objects.get(id=pk)
    checker = models.Usercart.objects.filter(user_id=request.user_id, user_product=current_product)

    if checker:
        checker[0].quantity = int(request.POST.get('pr_count'))
        checker[0].total_for_product = current_product.product_price * checker[0].quantity




    else:
        models.Usercart.objects.create(user_id=request.user_id, user_product=current_product, quantity=request.POST.get('pr_count'), total_for_product=int(current_product.product_price * request.POST.get('pr_count')))

     return redirect(f'/product-detail/{current_product.product_name}')

def get_user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)

    context ={'user_cart': user_cart}

    return render(request, 'cart.html', context)

def delete_pr_from_cart(request, pk):
    prod_to_delete = models.UserCart.objects.get(id=pk)

    prod_to_delete.delete()

    return redirect('/cart')

def order(request):
    invoice_message = '<b>Новый заказ</b>\n\n</b>Имя:</b> {username}\n<b>Номер:</b> {phone_number}\n<b>Адрес:'

    # for i in user_cart:
    #     invoice_message += '<b>{i.user_product}</b> x <b>{i.quantity} = {i.total_for_product}\n'

    invoice_message +='\n----------\n</b>Итог: {result} сум'


    # bot.send_message(921443677, invoice_message)
    return redirect ('/cart')

