from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from products.models import Product, Sizes, Cart, Order, PaymentOrder
from .forms import AddProductToCartForm, PlusAmountInCartListForm, MinusAmountInCartListForm, MakeOrderForm, \
    MakePaymentOrderForm
from django.contrib import messages


class ProductsViews(ListView):
    "Список товаров"
    model = Product
    queryset = Product.objects.all()  # SELECT * FROM Product


class ProductDetailView(DetailView):
    "Полная карточка товара"
    model = Product
    slug_field = "url"


class SizesView(DetailView):
    "Размеры товара"
    model = Sizes
    template_name = 'products/product_size.html'
    slug_field = "url"


class CartView(ListView):
    model = Cart

    def get_queryset(self): # Переопределяем queryset
        return Cart.objects.filter(cart_number=self.request.user.id).order_by('pk')


class CartToExistingOrderView(TemplateView):
    template_name = 'products/cart_to_existing_order.html'


class OrderView(ListView):
    "Размеры товара"
    model = Order
    template_name = 'products/order_list.html'
    def get_queryset(self): # Переопределяем queryset
        return Order.objects.filter(order_number=self.request.user.id).order_by('pk')


# Добавление 1 единицы товара в корзину пользователя
class AddProductToCartView(View):
    def post(self, request, pk):
        form = AddProductToCartForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product_id = pk
            form.cart_number = request.user.id
            form.price = form.product.price
            current_url = '/products/catalog/product/' + form.product.url


            # Обработка случая когда пользователь не авторизован
            if form.cart_number == None:
                return redirect("/accounts/login/")

            # Обработка случая когда не выбран размер
            if form.size == '--- Выбрать ---':
                messages.add_message(request, messages.WARNING, 'Вы не выбрали размер')
                return redirect(current_url)

            queryset_current_product_in_stock = Sizes.objects.filter(product=form.product_id,
                                                                     size=form.size)
            queryset_current_product = Cart.objects.filter(cart_number=request.user.id,
                                                           product_id=form.product_id,
                                                           size=form.size)

            # Если товара нету в наличии
            if len(queryset_current_product_in_stock) == 0:
                messages.add_message(request, messages.ERROR, 'Товара нет в наличии')
                return redirect(current_url)
            # Если количество товара в корзине равно количеству товара в наличии
            elif len(queryset_current_product_in_stock) == 1:
                current_product_in_stock = queryset_current_product_in_stock[0]
                if len(queryset_current_product) == 1:
                    current_product = queryset_current_product[0]
                    if current_product.amount == current_product_in_stock.amount_size:
                        messages.add_message(request, messages.ERROR, 'Товара нет в наличии')
                        return redirect(current_url)
                    # Стак одиновых товаров
                    current_product.amount = current_product.amount + 1
                    current_product.price = form.product.price * current_product.amount

                    messages.add_message(request, messages.SUCCESS, 'Товар добавлен в корзину')
                    current_product.save()
                    return redirect(current_url)

            #price_sum = Cart.objects.filter(cart_number=2).aggregate(Sum('price'))['price__sum']

            form.save()
            messages.add_message(request, messages.SUCCESS, 'Товар добавлен в корзину')
            return redirect(current_url)


# Увеличение количества товара в корзине пользователя на единицу"
class PlusAmountInCartListView(View):
    def post(self, request, pk):
        form = PlusAmountInCartListForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product_id = pk
            current_product = Cart.objects.filter(cart_number=request.user.id,
                                                  product_id=form.product_id,
                                                  size=form.size)[0]

            # Если количество товара в корзине равно количеству товара в наличии
            current_product_in_stock = Sizes.objects.filter(product_id=form.product_id,
                                                            size=form.size)[0]
            if current_product.amount == current_product_in_stock.amount_size:
                messages.add_message(request, messages.ERROR, 'Товара нет в наличии')
                return redirect('/products/cart/')

            current_product.amount = current_product.amount + 1
            current_product.price = form.product.price * current_product.amount
            current_product.save()
            return redirect('/products/cart/')


# Уменьшение количества товара в корзине пользователя на единицу
class MinusAmountInCartListView(View):
    def post(self, request, pk):
        form = MinusAmountInCartListForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product_id = pk
            current_product = Cart.objects.filter(cart_number=request.user.id,
                                                            product_id=form.product_id,
                                                            size=form.size)
            if len(current_product) > 0:
                current_product = current_product[0]
            else:
                return redirect('/products/cart/')

            # Если товар в корзине последний, то уменьшение его количества в корзине приведет к удалению товара
            if current_product.amount == 1:
                last_product = Cart.objects.filter(cart_number=request.user.id,
                                                   product_id=form.product_id,
                                                   size=form.size)
                last_product.delete()
                return redirect('/products/cart/')

            current_product.amount = current_product.amount - 1
            current_product.price = form.product.price * current_product.amount
            current_product.save()
            return redirect('/products/cart/')


class MakeOrderView(View):
    def post(self, request, pk):
        form = MakeOrderForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.product_id = pk

            if len(Order.objects.filter(order_number=request.user.id)) != 0:
                return redirect('/products/cart_to_existing_order/')

            queryset_user_cart = Cart.objects.filter(cart_number=request.user.id)

            for lines in queryset_user_cart:
                Order.objects.create(order_number=request.user.id, product=lines.product, size=lines.size,
                                     amount=lines.amount, price=lines.price)

        return redirect('/products/order/')


class DeleteOrderView(View):
    def post(self, request, pk):
        queryset_user_cart = Order.objects.filter(order_number=request.user.id)
        for line in queryset_user_cart:
            if line.order_number == request.user.id:
                line.delete()
        return redirect('/products/cart/')


class MakePaymentOrderView(View):
    def post(self, request, pk):
        form = MakePaymentOrderForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.payment_order_number = request.user.id
            form.payment_status = 'Не оплачено'
            form.delivery_status = 'Не доставлено'
            form.save()

        return redirect('/products/order/')
