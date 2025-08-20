from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from payments.mpesa import lipa_na_mpesa_online
from carts.models import CartItem
import datetime
from .forms import OrderForm

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If cart empty, redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # MPESA STK Push
            phone_number = '254745626529'  # test number, replace with actual customer phone later
            response = lipa_na_mpesa_online(phone_number, int(grand_total))

            if response.get('ResponseCode') == '0':
                # After STK push success, show thank you page
                context = {
                    'order': data,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total,
                }
                return render(request, 'orders/thank_you.html', context)
            else:
                messages.error(request, "Mpesa STK Push failed.")
                return redirect('checkout')

    else:
        return redirect('checkout')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from payments.mpesa import lipa_na_mpesa_online
from carts.models import CartItem
import datetime
from .forms import OrderForm

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If cart empty, redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # MPESA STK Push
            phone_number = '254745626529'  # test number, replace with actual customer phone later
            response = lipa_na_mpesa_online(phone_number, int(grand_total))

            if response.get('ResponseCode') == '0':
                # After STK push success, show thank you page
                context = {
                    'order': data,
                    'cart_items': cart_items,
                    'total': total,
                    'tax': tax,
                    'grand_total': grand_total,
                }
                return render(request, 'orders/thank_you.html', context)
            else:
                messages.error(request, "Mpesa STK Push failed.")
                return redirect('checkout')

    else:
        return redirect('checkout')
