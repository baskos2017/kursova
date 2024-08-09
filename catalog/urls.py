from django.urls import path
from . import views



urlpatterns = [
    path('product/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_summary, name='order_summary'),
    path('my_orders/', views.user_orders, name='user_orders'),
   
]
