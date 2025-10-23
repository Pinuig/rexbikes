from django.db import models
from products.models import Product
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    dated_added = models.DateTimeField(auto_now_add=True)
    # country = CountryField(blank_label='(select country)')
    # state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.cart_id} - {self.country} - {self.state}"
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    order_number = models.CharField(max_length=20, null=True, blank=True)
    billing_first_name = models.CharField(max_length=50, null=True, blank=True)
    billing_last_name = models.CharField(max_length=50, null=True, blank=True)
    billing_phone = models.CharField(max_length=15, null=True, blank=True, default='0123456789')
    billing_email = models.EmailField(max_length=50, null=True, blank=True, default='rexbmxbikecollection@gmail.com')
    billing_address = models.CharField(max_length=200, null=True, blank=True, default='101 Duval street, Key West, FL 33040')
    billing_city = models.CharField(max_length=100, null=True, blank=True, default='Key West')
    billing_company = models.CharField(max_length=100, null=True, blank=True, default='Rexbmx Bike Collection')
    shipping_first_name = models.CharField(max_length=50, null=True, blank=True)
    shipping_last_name = models.CharField(max_length=50, null=True, blank=True)
    shipping_phone = models.CharField(max_length=15, null=True)
    shipping_email = models.EmailField(max_length=50, null=True)
    shipping_address = models.CharField(max_length=200, null=True)
    shipping_city = models.CharField(max_length=100, null=True)
    shipping_company = models.CharField(max_length=100, null=True, blank=True)
    order_note = models.CharField(max_length=100, null=True, blank=True)
    order_total = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True, default="Cash on Delivery")
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return str(self.billing_first_name)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return str(self.product.product_name)
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_uses = models.PositiveIntegerField(default=1, help_text="Maximum number of times this coupon can be used.")
    used = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.code