from django.contrib import admin
from core.models import Furnizor, Product, Category, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
# import import_export
# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'price', 'featured', 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']

class FurnizorAdmin(admin.ModelAdmin):
    list_display = ['title', 'image'] 

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['price', 'product_status', 'order_date']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['price', 'invoice_no', 'product_status', 'item', 'qty', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Furnizor, FurnizorAdmin) 
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)