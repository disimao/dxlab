from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)

from .models import (
    User,
    Address,
    Store,
    Customer,
    Product,
    OrderItem,
    Order,
    BillingInformation,
)


@admin.register(User)
class UsersAdmin(UserAdmin):
    def username(self, instance):
        return instance.email

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    exclude = ('date_joined', 'username')
    ordering = [
        '-id'
    ]
    fieldsets = (
        ('User',
         {'fields': ('email',
                     'password',
                     'mobile_phone_number',
                     'contact_phone_number')
          }
         ),
        ('Others',
         {'fields': ('is_active',
                     'created_at',
                     'updated_at')
          }
         )
    )
    add_fieldsets = (
        (None,
         {'classes': ('wide',),
          'fields': ('email',
                     'password1',
                     'password2',
                     'mobile_phone_number',
                     'contact_phone_number',
                     )
          }
         ),
    )
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    list_display = ['email', 'mobile_phone_number', 'contact_phone_number', 'is_active', 'created_at', 'updated_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ['street_name', 'city', 'state', 'postal_code']


@admin.register(Store)
class StoresAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'user',
    ]
    search_fields = ['email']


@admin.register(Customer)
class CustomersAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'user',
    ]
    search_fields = ['email']


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    autocomplete_fields = [
        'store',
    ]
    search_fields = ['name', 'description']


@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'product',
    ]


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    extra = 4
    autocomplete_fields = [
        'product',
    ]


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]
    autocomplete_fields = [
        'customer',
    ]
    search_fields = [
        'customer',
    ]


@admin.register(BillingInformation)
class BillingInformationAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'billing_address',
    ]
