from rest_framework.viewsets import ModelViewSet
from .serializers import (
    UserSerializer,
    AddressSerializer,
    BillingInformationSerializer,
    StoreSerializer,
    CustomerSerializer,
    ProductSerializer,
    OrderItemSerializer,
    OrderSerializer
)
from dxlab.apps.core.models import (
    User,
    Address,
    BillingInformation,
    Store,
    Customer,
    Product,
    OrderItem,
    Order,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('pk')
    serializer_class = UserSerializer


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.order_by('pk')
    serializer_class = AddressSerializer


class BillingInformationViewSet(ModelViewSet):
    queryset = BillingInformation.objects.order_by('pk')
    serializer_class = BillingInformationSerializer


class StoreViewSet(ModelViewSet):
    queryset = Store.objects.order_by('pk')
    serializer_class = StoreSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.order_by('pk')
    serializer_class = CustomerSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.order_by('pk')
    serializer_class = OrderItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.order_by('pk')
    serializer_class = OrderSerializer
