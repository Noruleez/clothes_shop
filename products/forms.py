from django import forms

from .models import Cart, Order, PaymentOrder


class AddProductToCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('size',)


class PlusAmountInCartListForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('size',)


class MinusAmountInCartListForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('size',)


class MakeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('size',)


class MakePaymentOrderForm(forms.ModelForm):
    class Meta:
        model = PaymentOrder
        fields = ('delivery_address', 'delivery_period', 'phone_user',)
