from django.shortcuts import render, redirect
from django.conf import settings
from . models import Payment
import razorpay
from decimal import Decimal

# Create your views here.

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment_page(request):
    if request.method == 'POST':
        try:

            amount = Decimal(request.POST['amount']) * 100
            total_items = int(request.POST.get('total_items', 1))
        except (ValueError, KeyError):
            return render(request, 'payment_form.html', {'error': 'Invalid amount or total items value'})
        

        payment = Payment.objects.create(
            amount=amount / 100, 
            total_items=total_items, 
            payment_method='Razorpay')
        
        print("Razorpay Key ID:", settings.RAZORPAY_KEY_ID)
        print("Razorpay Key Secret:", settings.RAZORPAY_KEY_SECRET)

        #Razorpay order creation
        razorpay_order = razorpay_client.order.create(dict(
            amount=int(amount), 
            currency="INR", 
            payment_capture=1
        ))

        payment.razorpay_order_id = razorpay_order['id']
        payment.save()

        context = {
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'order_id': razorpay_order['id'],
            'amount': amount,
            'total_items': total_items,
        }
        return render(request, 'razorpay_payment.html', context)
    return render(request, 'payment_form.html')


def cod_payment(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST['amount'])
            total_items = int(request.POST.get('total_items', 1))

            Payment.objects.create(
                amount=amount, 
                total_items=total_items, 
                payment_method='COD', 
                payment_status ='Completed'
            )
            
            return redirect('payment_success')
        except (ValueError, KeyError):
            return render(request, 'payment_form.html', {'error': 'Invalid amount or total items value'})
    
    return redirect('payment_page')


def payment_success(request):
    return render(request, 'success.html')
    


