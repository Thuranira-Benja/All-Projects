# store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Order
from .mpesa_utils import lipa_na_mpesa_online
import json

def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'store/home.html', context)

def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock_quantity:
            # Handle error: not enough stock
            return render(request, 'store/product_detail.html', {'product': product, 'error': 'Not enough items in stock.'})

        total_price = product.price * quantity
        
        # Create a pending order
        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            customer_phone=phone_number,
        )

        # Initiate STK Push
        response = lipa_na_mpesa_online(
            phone_number=phone_number,
            amount=total_price,
            account_reference=f"DNEGO-{order.id}",
            transaction_desc=f"Payment for {product.name}"
        )

        if response and response.get('ResponseCode') == '0':
            order.checkout_request_id = response['CheckoutRequestID']
            order.save()
            # A message to show the user to check their phone
            message = "Success. Please check your phone to complete the M-PESA payment."
            return render(request, 'store/product_detail.html', {'product': product, 'message': message})
        else:
            order.status = 'failed'
            order.save()
            error_message = response.get('errorMessage', 'An unknown error occurred.')
            return render(request, 'store/product_detail.html', {'product': product, 'error': error_message})

    return render(request, 'store/product_detail.html', {'product': product})


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("MPESA Callback Data:", data) # For debugging

        try:
            callback_data = data['Body']['stkCallback']
            result_code = callback_data['ResultCode']
            checkout_request_id = callback_data['CheckoutRequestID']
            
            order = Order.objects.get(checkout_request_id=checkout_request_id)

            if result_code == 0:
                # Payment was successful
                metadata = callback_data['CallbackMetadata']['Item']
                mpesa_receipt = next(item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber')
                
                order.status = 'paid'
                order.mpesa_receipt_code = mpesa_receipt
                
                # Decrement product stock
                product = order.product
                product.stock_quantity -= order.quantity
                product.save()

            else:
                # Payment failed or was cancelled
                order.status = 'failed'

            order.save()

            return HttpResponse(status=200)

        except (KeyError, Order.DoesNotExist) as e:
            print(f"Callback error: {e}")
            return HttpResponse(status=400) # Bad request
            
    return HttpResponse(status=405) # Method not allowed


def contact(request):
    return render(request, 'store/contact.html')