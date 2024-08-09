from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    current_category = None

    if request.GET.get("category"):
        current_category = request.GET.get("category")
        products = products.filter(category__slug=current_category)

    if request.GET.get("search"):
        products = products.filter(name__icontains=request.GET.get("search"))

    if request.GET.get("min_price"):
        products = products.filter(price__gte=request.GET.get("min_price"))

    if request.GET.get("max_price"):
        products = products.filter(price__lte=request.GET.get("max_price"))

    data_form = {
        'search': request.GET.get("search", ""),
        'min_price': request.GET.get("min_price"),
        'max_price': request.GET.get("max_price"),
        'category': current_category
    }

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    viewed_products = []
    if request.user.is_authenticated:
        viewed_products = ViewedProduct.objects.filter(user=request.user).select_related('product')[:5]

    context = {
        'products': page_obj,
        'categories': categories,
        'data_form': data_form,
        'current_category': current_category,
        'viewed_products': viewed_products,
    }

    return render(request, 'catalog/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = product.comments.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = product
            new_comment.save()
            return redirect('product_detail', slug=product.slug)
    else:
        comment_form = CommentForm()

    # додаємо до історії переглядів
    if request.user.is_authenticated:
        ViewedProduct.objects.get_or_create(user=request.user, product=product)

    # отримуємо історію переглядів
    viewed_products = ViewedProduct.objects.filter(user=request.user).select_related('product')[:5]

    context = {
        'product': product,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'viewed_products': viewed_products,
    }

    return render(request, 'catalog/product_detail.html', context)



@login_required
def create_order(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_cost = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                item.delete()

            # Створення та відправлення електронного листа
            order_items = order.order_items.all()
            context = {
                'order': order,
                'order_items': order_items,
                'viewed_products': ViewedProduct.objects.filter(user=request.user).select_related('product')[:5]
            }
            email_subject = 'Підтвердження замовлення'
            email_body = render_to_string('catalog/order_summary_email.html', context)
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[request.user.email]
                
            )
            email.content_subtype = 'html' 
            email.send()

            return redirect('order_summary', order_id=order.id)
    else:
        form = OrderForm()

    context = {
        'order_form': form,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'viewed_products': ViewedProduct.objects.filter(user=request.user).select_related('product')[:5]
    }
    return render(request, 'catalog/order_create.html', context)

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('auth')

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Пошук або створення об'єкта CartItem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # Якщо CartItem вже існує, то збільшити кількість
    if not created:
        cart_item.quantity += 1
    
    cart_item.save()

    return redirect('product_detail', slug=product.slug)


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('auth')  # Перенаправлення на сторінку аутентифікації

    viewed_products = []
    if request.user.is_authenticated:
        viewed_products = ViewedProduct.objects.filter(user=request.user).select_related('product')[:5]
    
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {
        'cart_items': cart_items,
        'viewed_products': viewed_products
        }
    return render(request, 'catalog/view_cart.html', context)



def order_summary(request, order_id):
    # Перевіряємо, чи замовлення належить поточному користувачеві
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.order_items.all()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'catalog/order_summary.html', context)


def remove_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('view_cart')

def update_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            product_id = int(key.split('_')[1])
            quantity = int(value)
            product = get_object_or_404(Product, id=product_id)
            cart.update(product, quantity)
    return redirect('view_cart')

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'catalog/user_orders.html', context)
