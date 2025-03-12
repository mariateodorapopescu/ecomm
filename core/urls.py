from django.urls import path
from core.views import index, test_products_view, home_view, product_list, category_list, category_detail
from core import views

app_name = "core"

urlpatterns = [
    # path("ceva/", views.index), 
    path("", index, name="index"),
    path("products", product_list, name="product-list"),
    path("categories", category_list, name="category-list"),
    path("categories", category_list, name="categories"),  # Adaugă acest URL cu numele "categories"
    path('category/<str:category_id>/', views.category_detail, name='category_detail'),
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle-wishlist'),
    path('wishlist/', views.get_wishlist, name='get-wishlist'), 
    path('cart/', views.cart_view, name='cart'),
    path('cart/action/', views.cart_action, name='cart-action'),
    path('cart/count/', views.get_cart_count, name='get-cart-count'),
    path('cart/items/', views.get_cart_items, name='get-cart-items'),
    path("aaaa/", test_products_view, name='test_products'),
    path("aaa/", home_view, name='home'),
    # Here I'm telling it where to put that =)) beaware of the paths!
]
