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

    mobile_phone_number = models.IntegerField(unique=True, verbose_name=_('Mobile phone number'))
    contact_phone_number = models.IntegerField(blank=False, null=False, verbose_name=_('Contact phone number'))
    email = models.EmailField(unique=True, verbose_name=_('E-mail Address'))
    first_name = models.CharField(max_length=40, blank=True, verbose_name=_('First name'))
    last_name = models.CharField(max_length=40, blank=True, verbose_name=_('Last name'))


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        unique_together = (
            'mobile_phone_number', 
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
    additional_information = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('State'))
    postal_code = models.IntegerField(blank=False, null=False, verbose_name=_('Postal code'))
    state = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('State'))
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


class BillingInformation(models.Model):
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=False, null=False,
                                        verbose_name=_('Billing Address'))
    business_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Business name'))
    identification_number = models.IntegerField(blank=False, null=False, verbose_name=_('Identification Number'))


class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('User'))

    def __str__(self):
        return '{name}'.format(name=self.user.name)


class Customers(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('User'))
    billing_information = models.ForeignKey(BillingInformation, on_delete=models.PROTECT, blank=False, null=False,
                                            verbose_name=_('Billing Address'))
    shipping_address = models.ManyToManyField(Address, blank=False, verbose_name=_('Billing Address\''))

    def __str__(self):
        return '{name}'.format(name=self.user.name)


class Products(TimestampedModel, StatusModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True, verbose_name=_("Slug"))
    name = models.CharField(db_index=True, max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))

    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name='products'
    )

    def __str__(self):
        return self.name


class OrderItems(TimestampedModel):
    order = models.ForeignKey('Orders', on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('Order'))
    product = models.ForeignKey(Products, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('Product'))
    quantity = models.IntegerField(blank=False, null=False, verbose_name=_('Quantity'))


class Orders(TimestampedModel):
    customer = models.ForeignKey(Customers, on_delete=models.PROTECT, blank=False, null=False, verbose_name=_('Customer'))
    items = models.ManyToManyField(Products, through=OrderItems, blank=True, verbose_name=_('Items'))

    def __str__(self):
        return '{id} - {customer}'.format(id=self.id, customer=self.customer)
