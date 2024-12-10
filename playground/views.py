from django.shortcuts import render
from stor.models import Product, OrderItem

# Create your views here.
def say_hello(request):
    # Use the correct field name 'product_id'
    query_set = OrderItem.objects.values('product_id').distinct()
    # Render the response with the query set
    return render(request, 'say_hello.html', {'products': query_set})
