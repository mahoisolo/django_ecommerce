from rest_framework import serializers
from .models import Product,Collections,Review,Cart,CartItem,Customer,Order,OrderItem
from decimal import Decimal
from core.serializers import UserSerializer
class collections_serializer(serializers.ModelSerializer):
    class Meta:
        model=Collections
        fields=['id','title','product_count']
    product_count=serializers.IntegerField(read_only=True)    
class product_serializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','description','slug','inventory','price','price','tax_price','Collections']
    tax_price=serializers.SerializerMethodField(method_name='get_tax_price')
    def get_tax_price(self,product:Product):
        return product.price* Decimal(0.1)
    def create(self,validated_data):
        product=Product.objects.create(**validated_data)
        product.other=1
        product.save()
        return product
    def update(self,instance,validated_data):
        instance.unit_price=validated_data.get('unit_price')
        instance.save()
        return instance
class review_serializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','description','date']
    def create(self,validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']    
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','total_price']     
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # UUID field is read-only
    items = CartItemSerializer(many=True,source='cart_items',read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    def get_total_price(self,cart:Cart):
        return sum([item.quantity * item.product.price for item in cart.cart_items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items','total_price'] 
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
            self.instance=cart_item
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(cart_id=cart_id,**self.validated_data) 
        return self.instance       
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']       
class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']        
class CustomerSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)  # Include the related User object

    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership'] 
class OrderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price']        

                               
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=['id','customer','placed_at','payment_status','items']
