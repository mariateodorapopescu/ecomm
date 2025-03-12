# from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from core.models import Product, Category, Furnizor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

# Create your views here.

def index(request):
    # return HttpResponse('Hello, world!')
    # return HttpResponse('<h1 style="color:red">Hello, world!</h1>')
    # products = Product.objects.all()
    products = Product.objects.filter(featured=True)

    context = {
        "products": products # is the one from above
    }
    return render(request, 'core/index.html', context)
    # return None

# def product_list(request):
#     # return HttpResponse('Hello, world!')
#     # return HttpResponse('<h1 style="color:red">Hello, world!</h1>')
#     products = Product.objects.all()
#     # products = Product.objects.filter(featured=True)

#     context = {
#         "products": products # is the one from above
#     }
#     return render(request, 'core/product_list.html', context)
#     # return None

def get_filtered_products(request):
    """
    Funcție utilitară pentru a obține produsele filtrate și sortate
    """
    # Inițializăm query-ul de bază
    products_list = Product.objects.all()
    
    # Filtrare după preț
    price_range = request.GET.get('price', None)
    if price_range:
        try:
            max_price = float(price_range)
            products_list = products_list.filter(price__lte=max_price)
        except ValueError:
            pass
    
    # Filtrare după categorie
    category_ids = request.GET.getlist('category')
    if category_ids:
        category_filter = Q()
        for category_id in category_ids:
            try:
                category_filter |= Q(category__id=int(category_id))
            except ValueError:
                pass
        products_list = products_list.filter(category_filter)
    
    # Filtrare după disponibilitate în stoc
    in_stock = request.GET.get('in_stock')
    if in_stock == 'true':
        products_list = products_list.filter(in_stock=True)
    
    # Sortare
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price-low':
        products_list = products_list.order_by('price')
    elif sort_by == 'price-high':
        products_list = products_list.order_by('-price')
    elif sort_by == 'newest':
        products_list = products_list.order_by('-date')
    elif sort_by == 'popular':
        products_list = products_list.order_by('-featured', 'title')
    
    return products_list, sort_by, category_ids, price_range, in_stock

# def product_list(request):
#     # Obținem toate categoriile pentru filtre
#     categories = Category.objects.all()
    
#     # Inițializăm query-ul de bază
#     products_list = Product.objects.all()
    
#     # Filtrare după preț
#     price_range = request.GET.get('price', None)
#     if price_range:
#         try:
#             max_price = float(price_range)
#             products_list = products_list.filter(price__lte=max_price)
#         except ValueError:
#             # Ignorăm dacă prețul nu este un număr valid
#             pass
    
#     # Filtrare după categorie
#     category_ids = request.GET.getlist('category')
#     if category_ids:
#         category_filter = Q()
#         for category_id in category_ids:
#             try:
#                 category_filter |= Q(category__id=int(category_id))
#             except ValueError:
#                 # Ignorăm dacă ID-ul nu este un număr valid
#                 pass
#         products_list = products_list.filter(category_filter)
    
#     # Filtrare după disponibilitate în stoc
#     in_stock = request.GET.get('in_stock')
#     if in_stock == 'true':
#         products_list = products_list.filter(in_stock=True)
    
#     # Sortare
#     sort_by = request.GET.get('sort', 'default')
#     if sort_by == 'price-low':
#         products_list = products_list.order_by('price')
#     elif sort_by == 'price-high':
#         products_list = products_list.order_by('-price')
#     elif sort_by == 'newest':
#         products_list = products_list.order_by('-date')
#     elif sort_by == 'popular':
#         # Produsele populare sunt cele marcate ca "featured"
#         products_list = products_list.order_by('-featured', 'title')
    
#     # Paginare - 9 produse per pagină
#     paginator = Paginator(products_list, 9)
#     page = request.GET.get('page', 1)
    
#     try:
#         products = paginator.page(page)
#     except:
#         # În caz de erori, afișăm prima pagină
#         products = paginator.page(1)
    
#     # Construim contextul
#     context = {
#         'products': products,
#         'categories': categories,
#         'current_sort': sort_by,
#         'selected_categories': category_ids,
#         'current_price': price_range,
#         'show_in_stock': in_stock == 'true',
#     }
    
#     return render(request, 'core/product_list.html', context)

def product_list(request):
    # Preluăm produsele și alte date necesare
    products_list, sort_by, category_ids, price_range, in_stock = get_filtered_products(request)
    categories = Category.objects.all()
    
    # Creăm un set cu pid-urile produselor din wishlist
    wishlist_products_pids = set()
    if request.user.is_authenticated:
        wishlist_products_pids = set(
            Wishlist.objects.filter(user=request.user)
            .values_list('product__pid', flat=True)
        )
    
    # Marcăm produsele care sunt în wishlist
    for product in products_list:
        product.in_wishlist = product.pid in wishlist_products_pids
    
    # Restul codului pentru paginare etc...
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page', 1)
    
    try:
        products = paginator.page(page)
    except:
        products = paginator.page(1)
    
    context = {
        'products': products,
        'categories': categories,
        'current_sort': sort_by,
        'selected_categories': category_ids,
        'current_price': price_range,
        'show_in_stock': in_stock == 'true',
        'wishlist_products': wishlist_products_pids,  # Adăugăm lista de pid-uri în wishlist
    }
    
    return render(request, 'core/product_list.html', context)

def category_list(request):
    # return HttpResponse('Hello, world!')
    # return HttpResponse('<h1 style="color:red">Hello, world!</h1>')
    cats = Category.objects.all()
    # products = Product.objects.filter(featured=True)

    context = {
        "categories": cats # is the one from above
    }
    return render(request, 'core/categories_list.html', context)
    # return None

def category_detail(request, category_id):
    # Obținem categoria sau returnăm 404 dacă nu există
    # category = get_object_or_404(Category, id=category_id)
    category = get_object_or_404(Category, cid=category_id)
    
    # Preluăm toți furnizorii pentru filtre
    vendors = Furnizor.objects.all()
    
    # Inițializăm query-ul pentru produse cu filtrarea de bază după categorie
    products_list = Product.objects.filter(category=category, status=True)
    
    # Filtrare după preț
    price_range = request.GET.get('price', None)
    if price_range:
        try:
            max_price = float(price_range)
            products_list = products_list.filter(price__lte=max_price)
        except ValueError:
            # Ignorăm dacă prețul nu este un număr valid
            pass
    
    # Filtrare după furnizor (vendor)
    vendor_ids = request.GET.getlist('vendor')
    if vendor_ids:
        vendor_filter = Q()
        for vendor_id in vendor_ids:
            try:
                vendor_filter |= Q(vendor__id=int(vendor_id))
            except ValueError:
                # Ignorăm dacă ID-ul nu este un număr valid
                pass
        products_list = products_list.filter(vendor_filter)
    
    # Filtrare după disponibilitate în stoc
    in_stock = request.GET.get('in_stock')
    if in_stock == 'true':
        products_list = products_list.filter(in_stock=True)
    
    # Sortare
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price-low':
        products_list = products_list.order_by('price')
    elif sort_by == 'price-high':
        products_list = products_list.order_by('-price')
    elif sort_by == 'newest':
        products_list = products_list.order_by('-date')
    elif sort_by == 'popular':
        # Presupunem că produsele populare sunt cele marcate ca "featured"
        products_list = products_list.order_by('-featured', 'title')
    
    # Paginare - 9 produse pe pagină
    paginator = Paginator(products_list, 3)
    page = request.GET.get('page', 1)
    
    try:
        products = paginator.page(page)
    except:
        # În caz de erori, afișăm prima pagină
        products = paginator.page(1)
    
    # Construim contextul
    context = {
        'category': category,
        'products': products,
        'vendors': vendors,
        'current_sort': sort_by,
        'selected_vendors': vendor_ids,
        'current_price': price_range,
        'show_in_stock': in_stock == 'true',
    }
    
    return render(request, 'core/category_explore.html', context)

def test_products_view(request):
    all_products = Product.objects.all()
    
    html = """
    <html>
    <head><title>Test Produse</title></head>
    <body>
        <h1>Lista produse în baza de date:</h1>
    """
    
    if all_products.exists():
        html += f"<p>Număr total produse: {all_products.count()}</p><ul>"
        for p in all_products:
            html += f"<li>ID: {p.id}, Titlu: {p.title}, Status: {p.status}, Preț: {p.price}</li>"
        html += "</ul>"
    else:
        html += "<p>Nu există produse în baza de date!</p>"
    
    html += """
    </body>
    </html>
    """
    
    return HttpResponse(html)

# Django uses views, templates and urls to create a page, 
# therefore whenever you want to craete a page you have to create a view for it

def home_view(request):
      # Verificați toate produsele
    all_products = Product.objects.all()
    
    # Folosiți același filtru ca în view-ul original
    filtered_products = Product.objects.filter(status=True)
    
    html = """
    <html>
    <head>
        <title>Test Produse</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .section { margin-bottom: 30px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
            .product { margin-bottom: 10px; padding: 10px; background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Test Afișare Produse</h1>
    """
    
    # Secțiunea 1: Toate produsele
    html += """
        <div class="section">
            <h2>Toate produsele din baza de date:</h2>
    """
    
    if all_products.exists():
        html += f"<p>Număr total produse: {all_products.count()}</p><ul>"
        for p in all_products:
            html += f"""
            <div class="product">
                <p><strong>ID:</strong> {p.id}</p>
                <p><strong>Titlu:</strong> {p.title}</p>
                <p><strong>Status:</strong> {p.status}</p>
                <p><strong>Status produs:</strong> {p.product_status}</p>
                <p><strong>Preț:</strong> {p.price}</p>
                <p><strong>Preț vechi:</strong> {p.old_price}</p>
                <p><strong>Categorie:</strong> {p.category.title if p.category else 'Nicio categorie'}</p>
                <p><strong>Utilizator:</strong> {p.user.username if p.user else 'Niciun utilizator'}</p>
            </div>
            """
        html += "</ul>"
    else:
        html += "<p>Nu există produse în baza de date!</p>"
    
    # Secțiunea 2: Produse filtrate
    html += """
        </div>
        <div class="section">
            <h2>Produse filtrate (status=True):</h2>
    """
    
    if filtered_products.exists():
        html += f"<p>Număr produse filtrate: {filtered_products.count()}</p>"
        for p in filtered_products:
            html += f"""
            <div class="product">
                <p><strong>ID:</strong> {p.id}</p>
                <p><strong>Titlu:</strong> {p.title}</p>
                <p><strong>Status:</strong> {p.status}</p>
                <p><strong>Status produs:</strong> {p.product_status}</p>
                <p><strong>Preț:</strong> {p.price}</p>
            </div>
            """
    else:
        html += "<p>Nu există produse care să corespundă filtrelor!</p>"
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html)

@login_required
@require_POST
def toggle_wishlist(request):
    """
    View pentru adăugarea/eliminarea unui produs din lista de dorințe
    """
    product_id = request.POST.get('product_id')
    
    print(f"ID primit: {product_id}, tip: {type(product_id)}")
    
    if not product_id:
        return JsonResponse({'success': False, 'message': 'ID produs lipsă'}, status=400)
    
    try:
        # Încearcă să obții produsul și printează ce găsești
        print(f"Căutăm produsul cu pid: {product_id}")
        product_exists = Product.objects.filter(pid=product_id).exists()
        print(f"Produsul există: {product_exists}")
        
        if not product_exists:
            # Afișează toate PID-urile existente pentru debug
            all_pids = list(Product.objects.values_list('pid', flat=True))
            print(f"PID-uri existente: {all_pids}")
            return JsonResponse({'success': False, 'message': 'Produsul nu a fost găsit'}, status=404)
        
        product = Product.objects.get(pid=product_id)
        
        # Verificăm dacă produsul este deja în lista de dorințe
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        
        if wishlist_item:
            # Dacă există deja, îl ștergem
            wishlist_item.delete()
            return JsonResponse({
                'success': True, 
                'added': False,
                'message': 'Produs eliminat din lista de dorințe'
            })
        else:
            # Altfel, îl adăugăm
            Wishlist.objects.create(user=request.user, product=product)
            return JsonResponse({
                'success': True, 
                'added': True,
                'message': 'Produs adăugat în lista de dorințe'
            })
            
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Produsul nu a fost găsit'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Eroare: {str(e)}'
        }, status=500)

@login_required
def get_wishlist(request):
    """
    View pentru obținerea listei de dorințe a utilizatorului
    """
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    products = []
    for item in wishlist_items:
        products.append({
            'pid': item.product.pid,
            'title': item.product.title,
            'price': float(item.product.price),
            'image': item.product.image.url if item.product.image else None,
        })
    
    return JsonResponse({
        'success': True,
        'count': len(products),
        'products': products
    })

def get_cart_count(request):
    """Get the number of items in the user's cart"""
    if request.user.is_authenticated:
        # For logged in users, get from database
        cart_items = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False)
        cart_count = sum(item.qty for item in cart_items)
    else:
        # For anonymous users, get from session
        cart = request.session.get('cart', {})
        cart_count = sum(item.get('qty', 0) for item in cart.values())
    
    return JsonResponse({
        'success': True,
        'cart_count': cart_count
    })

# @login_required
# def cart_action(request):
#     """Add, remove, or update cart items"""
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         action = request.POST.get('action', 'add')
        
#         try:
#             product = Product.objects.get(pid=product_id)
            
#             # Get or create cart order
#             cart_order, created = CartOrder.objects.get_or_create(
#                 user=request.user,
#                 paid_status=False
#             )
            
#             if action == 'add':
#                 # Check if item already in cart
#                 try:
#                     cart_item = CartOrderItems.objects.get(
#                         order=cart_order,
#                         item=product.title
#                     )
#                     # Item exists, increment quantity
#                     cart_item.qty += 1
#                     cart_item.total = cart_item.qty * float(cart_item.price)
#                     cart_item.save()
#                     message = f"{product.title} cantitate actualizată în coș"
#                 except CartOrderItems.DoesNotExist:
#                     # Item doesn't exist, create new
#                     cart_item = CartOrderItems.objects.create(
#                         order=cart_order,
#                         invoice_no=f"INV-{cart_order.id}",
#                         item=product.title,
#                         image=product.image.url,
#                         price=product.price,
#                         qty=1,
#                         total=product.price
#                     )
#                     message = f"{product.title} adăugat în coș"
            
#             elif action == 'remove':
#                 # Remove item from cart
#                 try:
#                     cart_item = CartOrderItems.objects.get(
#                         order=cart_order,
#                         item=product.title
#                     )
#                     cart_item.delete()
#                     message = f"{product.title} șters din coș"
#                 except CartOrderItems.DoesNotExist:
#                     message = "Produsul nu există în coș"
            
#             # Update order total price
#             cart_order.price = sum(float(item.total) for item in CartOrderItems.objects.filter(order=cart_order))
#             cart_order.save()
            
#             # Get updated cart count
#             cart_count = sum(item.qty for item in CartOrderItems.objects.filter(order=cart_order))
            
#             return JsonResponse({
#                 'success': True,
#                 'message': message,
#                 'cart_count': cart_count
#             })
            
#         except Product.DoesNotExist:
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Produsul nu a fost găsit'
#             })
    
#     return JsonResponse({
#         'success': False,
#         'message': 'Metoda nepermisă'
#     })

@login_required
def cart_action(request):
    """Add, remove, or update cart items"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action', 'add')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(pid=product_id)
            
            # Get or create cart order
            cart_order, created = CartOrder.objects.get_or_create(
                user=request.user,
                paid_status=False
            )
            
            if action == 'add' or action == 'update':
                # Check if item already in cart
                try:
                    cart_item = CartOrderItems.objects.get(
                        order=cart_order,
                        item=product.title
                    )
                    
                    if action == 'update':
                        # Update quantity directly
                        cart_item.qty = quantity
                    else:
                        # Increment quantity
                        cart_item.qty += quantity
                        
                    cart_item.total = cart_item.qty * float(cart_item.price)
                    cart_item.save()
                    message = f"{product.title} cantitate actualizată în coș"
                except CartOrderItems.DoesNotExist:
                    # Item doesn't exist, create new
                    cart_item = CartOrderItems.objects.create(
                        order=cart_order,
                        invoice_no=f"INV-{cart_order.id}",
                        item=product.title,
                        image=product.image.url,
                        price=product.price,
                        qty=quantity,
                        total=product.price * quantity
                    )
                    message = f"{product.title} adăugat în coș"
            
            elif action == 'remove':
                # Remove item from cart
                try:
                    cart_item = CartOrderItems.objects.get(
                        order=cart_order,
                        item=product.title
                    )
                    cart_item.delete()
                    message = f"{product.title} șters din coș"
                except CartOrderItems.DoesNotExist:
                    message = "Produsul nu există în coș"
            
            # Update order total price
            cart_items = CartOrderItems.objects.filter(order=cart_order)
            cart_order.price = sum(float(item.total) for item in cart_items)
            cart_order.save()
            
            # Get updated cart count
            cart_count = sum(item.qty for item in cart_items)
            
            # Get item quantity for the updated/added item
            item_quantity = 0
            try:
                if action != 'remove':
                    item = CartOrderItems.objects.get(order=cart_order, item=product.title)
                    item_quantity = item.qty
            except CartOrderItems.DoesNotExist:
                pass
                
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_count': cart_count,
                'item_quantity': item_quantity
            })
            
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Produsul nu a fost găsit'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Metoda nepermisă'
    })

def get_cart_items(request):
    """Get all items in the user's cart"""
    if request.user.is_authenticated:
        # For logged in users, get from database
        cart_items = CartOrderItems.objects.filter(order__user=request.user, order__paid_status=False)
        items = []
        
        for item in cart_items:
            # Get product ID from title
            try:
                product = Product.objects.get(title=item.item)
                product_id = product.pid
            except Product.DoesNotExist:
                product_id = None
                
            items.append({
                'product_id': product_id,
                'title': item.item,
                'price': float(item.price),
                'quantity': item.qty,
                'total': float(item.total),
                'image': item.image
            })
            
        return JsonResponse({
            'success': True,
            'cart_items': items,
            'cart_count': sum(item.qty for item in cart_items)
        })
    else:
        # For anonymous users, get from session
        cart = request.session.get('cart', {})
        items = []
        
        for product_id, item_data in cart.items():
            items.append({
                'product_id': product_id,
                'title': item_data.get('title', ''),
                'price': item_data.get('price', 0),
                'quantity': item_data.get('qty', 0),
                'total': item_data.get('total', 0),
                'image': item_data.get('image', '')
            })
            
        return JsonResponse({
            'success': True,
            'cart_items': items,
            'cart_count': sum(item.get('qty', 0) for item in cart.values())
        })

@login_required
def cart_view(request):
    """
    View for displaying the cart page
    """
    # Get cart items for the user
    cart_items = CartOrderItems.objects.filter(
        order__user=request.user,
        order__paid_status=False
    ).select_related('order')
    
    # Calculate totals
    subtotal = sum(float(item.total) for item in cart_items)
    shipping = 15.00  # Exemplu de cost de livrare fix
    total = subtotal + shipping
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    
    return render(request, 'core/cart.html', context)