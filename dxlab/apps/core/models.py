from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class TimestampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        abstract = True

        ordering = [
            '-created_at',
            '-updated_at',
        ]


class StatusModel(models.Model):
    
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        abstract = True

        ordering = [
            '-is_active',
        ]


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel, StatusModel):

    first_name = models.CharField(max_length=40, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=40, blank=True, verbose_name=_('Last name'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Active'))
    email = models.EmailField(unique=True, verbose_name=_('E-mail Address'))
    mobile_phone_number = models.IntegerField(blank=True, null=True, verbose_name=_('Mobile phone number'))
    contact_phone_number = models.IntegerField(blank=False, null=False, verbose_name=_('Contact phone number'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'contact_phone_number',
    ]

    class Meta:
        unique_together = (
            'email',
            )
        ordering = [
            '-id'
        ]

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return self.email


class Address(models.Model):
    street_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Street name'))
    number = models.IntegerField(blank=True, null=True, verbose_name=_('Number'))
    additional_information = models.CharField(max_length=255, blank=False, null=False,
                                              verbose_name=_('Additional Information'))
    postal_code = models.IntegerField(blank=False, null=False, verbose_name=_('Postal code'))
    state = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('State'))
    city = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('City'))
    country = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('Country'))

    class Meta:
        unique_together = (
            'street_name', 
            'number', 
            'additional_information',
            'postal_code', 
            'state', 
            'country'
            )
        ordering = [
            '-id'
        ]

    def __str__(self):
        return self.street_name


class BillingInformation(models.Model):
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=False, null=False,
                                        verbose_name=_('Billing Address'))
    business_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Business name'))
    identification_number = models.CharField(max_length=55, blank=False, null=False, verbose_name=_('Identification Number'))

    def __str__(self):
        return '{} - {}'.format(self.billing_address, self.identification_number)


class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('User'))
    products = models.ManyToManyField(
        'Product', blank=models.PROTECT, related_name='store'
    )

    def __str__(self):
        return '{name}'.format(name=self.user.email)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('User'))
    billing_information = models.ForeignKey(BillingInformation, on_delete=models.PROTECT, blank=False, null=False,
                                            verbose_name=_('Billing Address'))
    shipping_address = models.ManyToManyField(Address, blank=True, verbose_name=_('Shipping Address\''))

    def __str__(self):
        return '{name}'.format(name=self.user.email)


class Product(TimestampedModel, StatusModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True, verbose_name=_("Slug"))
    name = models.CharField(db_index=True, max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))

    def __str__(self):
        return self.name


class OrderItem(TimestampedModel):
    order = models.ForeignKey('Order', on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('Product'))
    quantity = models.IntegerField(blank=False, null=False, verbose_name=_('Quantity'))

    def __str__(self):
        return '{order}'.format(order=self.order.id)


class Order(TimestampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('Customer'))
    items = models.ManyToManyField(Product, through=OrderItem, blank=True, verbose_name=_('Items'))

    def __str__(self):
        return '{id} - {customer}'.format(id=self.id, customer=self.customer)
