from django.contrib import admin
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
# from uuid import uuid4
import uuid  # Import the uuid module

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Collections(models.Model):
    title=models.CharField(max_length=120)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+' )
    # product=models.ForeignKey(Product,on_delete=models.PROTECT) 
    def __str__(self)-> str:
        return self.title
    class meta:
        ordering=['title']
class Product(models.Model):
    title=models.CharField(max_length=120)
    slug=models.SlugField()
    description=models.TextField(blank=True,null=True)
    price = models.DecimalField(decimal_places=6, max_digits=12,validators=[MinValueValidator(1)])  
    inventory=models.IntegerField()
    last_update=models.DateField(auto_now=True)
    Collections=models.ForeignKey(Collections,on_delete=models.CASCADE)
    promotions=models.ManyToManyField(Promotion,blank=True)
    def __str__(self)-> str:
        return self.title
    class meta:
        ordering=['title']

class Customer(models.Model):
    bronze_membership='B'
    silver_membership='S'
    gold_membership='G'
    MEMBERSHIP_CHOICES=[
        (bronze_membership,'Bronze'),
        (silver_membership,'Silver'),
        (gold_membership,'Gold')

    ]
 
    phone=models.CharField(max_length=120)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default='B')
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self)-> str:
        return self.user.first_name
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    class meta:
        ordering=['user_first_name']
class Order(models.Model):
    payment_status_pending='p'
    payment_status_complete='c'
    payment_status_failed='f'
    STATUS_CHOICE=[
        (payment_status_pending,'Pending'),
        (payment_status_complete,'Completed'),
        (payment_status_failed,'Failed'),
    ]
    placed_at=models.DateTimeField(auto_now_add=True) 
    payment_status=models.CharField(max_length=1,choices=STATUS_CHOICE) 
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)
    class Meta:
        permissions=[
            ('cancel_order','Can cancel order')]  
# from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE, primary_key=True)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.JSONField(default=dict)  # No conflict with related_name='cart_items'

    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')  # Avoid name conflict
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]  # Ensures one product per cart

    def __str__(self):
        return f"{self.product} (x{self.quantity})"
       
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=255)    
    description=models.TextField()
    date=models.DateField(auto_now_add=True)