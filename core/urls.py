from django.urls import path
from core.views import index, test_products_view, home_view, product_list, category_list, category_detail, cart_action, get_cart_items, get_cart_count, cart_view
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

    path('cart/items/', get_cart_items, name='get_cart_items'),
    path('cart/count/', get_cart_count, name='get_cart_count'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/action/', cart_action, name='cart_action'),

    path("aaaa/", test_products_view, name='test_products'),
    path("aaa/", home_view, name='home'),
    # Here I'm telling it where to put that =)) beaware of the paths!
]
