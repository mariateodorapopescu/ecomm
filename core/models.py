from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE=(
    ("incurs", "In curs de procesare..."),
    ("livrat", "Livrat"),
    ("trimis", "Pus la curier"),
)

STATUS=(
    ("wip", "Schita"),
    ("disabled", "Blocat"),
    ("anulat", "Anulat"),
    ("review", "In curs de verificare"),
    ("published", "Incarcat"),
)

RATING=(
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

# Create your models here.

def user_directory_path(instance, filename):
    # return 'user_{0}/{1}'.format(instance.user.id, filename)
    return f"user_{instance.user.id}/{filename}"

class Category(models.Model):
    # cid = models.UUIDField(unique=True)
    # cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    cid = ShortUUIDField(unique=True, length=10, alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="[Categorie]")
    image = models.ImageField(upload_to="categorie")

    class Meta:
        verbose_name_plural = "Categorii"
    
    def category_image(self):
        # return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Etichete"
    
    # def category_image(self):
    #     # return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    #     return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.name

class Furnizor(models.Model):
    # vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    vid = ShortUUIDField(unique=True, length=10, alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=100, default="[Furnizor]")
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null=True, blank=True, default="[Descriere furnizor]")

    address = models.CharField(max_length=100, default="[Bd. Preciziei nr. 24, Bloc A1, Ap.709]")
    contact = models.CharField(max_length=100, default="[+40 (787) 763 178]")
    chat_resp_time = models.CharField(max_length=100, default="[100]")
    shipping_on_time = models.CharField(max_length=100, default="[60]")
    authentic_rating = models.CharField(max_length=100, default="[5]")
    days_return = models.CharField(max_length=100, default="[30]")
    warranty_period = models.CharField(max_length=100, default="[30]")

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
   
    price = models.DecimalField(max_digits=10, decimal_places=2,default="00.00")
    old_price = models.DecimalField(max_digits=10, decimal_places=2,default="01.00")

    class Meta:
        verbose_name_plural = "Furnizori"
    
    def vendor_image(self):
        # return [mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))]
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    # pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345", default="produs nou")
    pid = ShortUUIDField(unique=True, length=10, alphabet="abcdefgh12345", default="[Produs nou]")
    
    title = models.CharField(max_length=100, default="[Produs]")
    image = models.ImageField(upload_to=user_directory_path, default="[Produs.jpg]")
    description = models.TextField(null=True, blank=True, default="[Descriere produs]")

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    vendor = models.ForeignKey(Furnizor, on_delete = models.SET_NULL, null = True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default="00.00")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default="01.00")

    specifications = models.TextField(null=True, blank=True, default="[Alte specificatii]")
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="wip")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    # sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    sku = ShortUUIDField(unique=True, length=4, alphabet="1234567890")
    date = models.DateField(auto_now_add=True)
    updated = models.DateField(null = True, blank=True)

    class Meta:
        verbose_name_plural = "Produse"
    
    def product_image(self):
        # return [mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))]
        # return [mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url))]
        return mark_safe(f'<img src="{self.image.url}" width="50" height="50" />')
    
    def __str__(self):
        return self.title
    
    def get_precentage(self):
        # de verificat pentru /0
        if self.old_price and self.price > 0:
            new_price = 100 - (self.price / self.old_price) * 100
            return new_price
        return 0

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="produs.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="imagini")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Imagine produs"

# ################################################################################

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default="00.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="in curs de procesare")

    class Meta:
        verbose_name_plural = "Comanda"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete = models.CASCADE)
    invoice_no = models.CharField(max_length=(120))
    product_status = models.CharField(max_length=200)    
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default="01.99")
    total = models.DecimalField(max_digits=10, decimal_places=2, default="01.99")
    
    class Meta:
        verbose_name_plural = "Cos cumparaturi"
    
    def cmd_image(self):
        # return [mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))]
        return mark_safe(f'<img src={self.image} width="50" height="50" />')

# ################################################################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    review = models.TextField(null=True, blank=True) # ????
    rating = models.IntegerField(choices=RATING, default=3) # ?
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Review-uri produs"
    
    def __str__(self):
        return self.product.title

    def getRating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Lista dorinte"
    
    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length=255, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Adresa"
    
    def __str__(self):
        return self.product.address
