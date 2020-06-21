from rest_framework.routers import SimpleRouter
from .views import *


router = SimpleRouter()

router.register(r'user', UserViewSet)
router.register(r'address', AddressViewSet)
router.register(r'billinginformation', BillingInformationViewSet)
router.register(r'store', StoreViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'product', ProductViewSet)
router.register(r'orderitem', OrderItemViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = router.urls
