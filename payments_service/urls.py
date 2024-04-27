from django.urls import path, include
from rest_framework import routers

from payments_service.views import PaymentViewSet

app_name = "payments-service"

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
