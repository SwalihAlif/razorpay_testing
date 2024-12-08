from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment_page'),
    path('cod/', views.cod_payment, name='cod_payment'),
    path('success/', views.payment_success, name='payment_success'),
]