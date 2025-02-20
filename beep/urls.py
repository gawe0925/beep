from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from store.views import CustomerViewSet, CustomerUpdateView, ProductViewSet, OrderViewSet


router = DefaultRouter()
# create
router.register(r'create_customer', CustomerViewSet, basename="create")
# list
router.register(r'customer', CustomerViewSet, basename="list")
# update
router.register(r'update_customer/<int:pk>/', CustomerViewSet, basename="update")
router.register(r'product', ProductViewSet)
router.register(r'order', OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include("rest_framework.urls")),
]
