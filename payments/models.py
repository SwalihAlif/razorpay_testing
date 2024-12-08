from django.db import models

# Create your models here.

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_items = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=20, choices=[('Razorpay', 'Razorpay'), ('COD', 'Cash On Delivery')])
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.payment_method}"