from django.urls import path, include

from . import views


urlpatterns = [
    path("catalog/", views.ProductsViews.as_view(), name="catalog"),
    path("catalog/product/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("catalog/product/size/<str:slug>/", views.SizesView.as_view(), name="product_size"),
    path("cart/", views.CartView.as_view(), name="product_cart"),
    path("cart_to_existing_order/", views.CartToExistingOrderView.as_view(), name="cart_to_existing_order"),
    path("order/", views.OrderView.as_view(), name="product_order"),
    path("deleteorder<int:pk>/", views.DeleteOrderView.as_view(), name="delete_order"),
    path("makepaymentorder<int:pk>/", views.MakePaymentOrderView.as_view(), name="make_payment_order"),
    path("makeorder<int:pk>/", views.MakeOrderView.as_view(), name="make_order"),
    path("producttocart<int:pk>/", views.AddProductToCartView.as_view(), name="add_product_to_cart"),
    path("productincartplus<int:pk>/", views.PlusAmountInCartListView.as_view(), name="plus_amount_product_in_cart"),
    path("productincartminus<int:pk>/", views.MinusAmountInCartListView.as_view(), name="minus_amount_product_in_cart"),
]
