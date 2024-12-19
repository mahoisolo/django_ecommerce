from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet ,GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from uuid import UUID
from .models import Product, Collections, OrderItem, Review,Cart,CartItem,Customer,Order
from .serializer import product_serializer, collections_serializer, review_serializer, CartSerializer, CartItemSerializer, AddCartItemSerializer,CustomerSerializer,OrderSerializer
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly,FullDjangoModelFunction
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = product_serializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    pagination_class=PageNumberPagination
    permission_classes=[IsAdminOrReadOnly]
    search_fields=['title','description']
    ordering_fields=['price','last_update']
   

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).exists():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collections.objects.annotate(products_count=Count('product')).all()
    serializer_class = collections_serializer
    permission_classes=[IsAdminOrReadOnly]


    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).exists():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = review_serializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
class CartViewSet(CreateModelMixin,ListModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('cart_items__product')  
    serializer_class = CartSerializer
class CartItemsViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemSerializer
        elif self.request.method == 'PATCH':
            return AddCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    def get_queryset(self):
        return CartItem.objects \
    .filter(cart_id=self.kwargs['cart_pk']) \
    .select_related('product')

class CustomerViewSet(ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    permission_classes=[IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return[IsAuthenticated()]

    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=401)
        
        (customer,created)=Customer.objects.get_or_create(user_id=request.user.id)
        if request.method=='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method=='PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
class OrderViewSet(ModelViewSet):
    queryset=Order.objects.all()    
    serializer_class=OrderSerializer
