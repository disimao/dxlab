from rest_framework.serializers import ModelSerializer
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


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        depth = 2
        fields = ['first_name',
                  'last_name',
                  'email',
                  'contact_phone_number',
                  'mobile_phone_number'
                  ]


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        depth = 2
        fields = '__all__'


class BillingInformationSerializer(ModelSerializer):

    class Meta:
        model = BillingInformation
        depth = 2
        fields = '__all__'


class StoreSerializer(ModelSerializer):

    class Meta:
        model = Store
        depth = 2
        fields = '__all__'


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        depth = 2
        fields = '__all__'


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        depth = 2
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        depth = 2
        fields = '__all__'


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        depth = 2
        fields = '__all__'
