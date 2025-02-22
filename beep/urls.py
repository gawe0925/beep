from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from store.views import CustomerViewSet, ProductViewSet, OrderViewSet


router = DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'product', ProductViewSet)
router.register(r'order', OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include("rest_framework.urls")),
]
