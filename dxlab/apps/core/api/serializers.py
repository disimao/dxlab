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
        fields = [
            'id',
            'first_name',
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
    billing_address = AddressSerializer()

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
    user = UserSerializer()
    billing_information = BillingInformationSerializer()
    shipping_address = AddressSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        user_validated_data = validated_data.pop('user')
        user = User.objects.create(**user_validated_data)
        billing_info_validated_data = validated_data.pop('billing_information')
        billing_address_validated_data = billing_info_validated_data.pop('billing_address')
        billing_address = Address.objects.create(**billing_address_validated_data)
        billing_info_validated_data['billing_address'] = billing_address
        billing_info = BillingInformation.objects.create(**billing_info_validated_data)
        validated_data['user'] = user
        validated_data['billing_information'] = billing_info
        shipping_addres_validated_data = validated_data.pop('shipping_address')
        shipping_address = []
        for address in shipping_addres_validated_data:
            shipping_address.append(Address.objects.create(**address))
        instance = Customer.objects.create(**validated_data)
        instance.shipping_address.set(shipping_address)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        user_validated_data = validated_data.pop('user')
        User.objects.filter(id=instance.user.id).update(**user_validated_data)
        billing_info_validated_data = validated_data.pop('billing_information')
        billing_address_validated_data = billing_info_validated_data.pop('billing_address')
        Address.objects.filter(id=instance.billing_information.billing_address.id).update(**billing_address_validated_data)
        BillingInformation.objects.filter(id=instance.billing_information.id).update(**billing_info_validated_data)
        shipping_addres_validated_data = validated_data.pop('shipping_address')
        for address in shipping_addres_validated_data:
            Address.objects.create(**address)
        return Customer.objects.get(id=instance.id)


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
