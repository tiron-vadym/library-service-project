from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from payments_service.models import Payment
from payments_service.serializers import PaymentSerializer
import stripe


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Payment.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(borrowing__user=self.request.user)
        return queryset

    @action(detail=True, methods=["get"], url_path="success")
    def success(self, request):
        # payment = Payment.objects.get(id=pk)
        # session = stripe.checkout.Session.retrieve(payment.session_id)
        # if session.payment_status == "paid":
        #     payment.status = "PAID"
        #     payment.save()
        #     return Response(
        #         {"message": "Payment success"}, status=status.HTTP_200_OK
        #     )
        return Response(
            {"message": "Payment wasn't paid"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["get"], url_path="cancel")
    def cancel(self, request):
        return Response(
            {"message": "Payment can be paid a bit later"},
            status=status.HTTP_200_OK
        )
