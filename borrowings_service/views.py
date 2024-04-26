from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.db.models import Q

from borrowings_service.models import Borrowing
from borrowings_service.serializers import (
    ExtendedBorrowingSerializer,
    BorrowingSerializer,
    ReturnBorrowingSerializer,
)
from borrowings_service.permissions import IsOwner
from utilities.bot import send_message
from utilities.stripe import stripe_helper, pay_fine


class BorrowingCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Borrowing.objects.all().select_related("book", "user")
    serializer_class = ExtendedBorrowingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        book = serializer.validated_data["book"]
        if book:
            if book.inventory > 0:
                book.inventory -= 1
                book.save()
            else:
                return Response(
                    {"error": "Book out of stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        borrowing_id = serializer.data.get("id")
        borrowing = Borrowing.objects.get(id=borrowing_id)
        stripe_helper(borrowing)
        send_message("Well done! New borrowing created!")
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.query_params.get("user")
        is_active = self.request.query_params.get("is_active")
        queryset = Borrowing.objects.all()

        if user:
            if not self.request.user.is_staff:
                raise PermissionDenied(
                    "You are not authorized to use these parameters."
                )
            queryset = queryset.filter(user=user)
        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active == "false":
            queryset = queryset.filter(~Q(actual_return_date__isnull=True))

        return queryset.select_related("book", "user")


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all().select_related("book", "user")
    serializer_class = ExtendedBorrowingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Borrowing, pk=kwargs["pk"])
        if instance.expected_return_date < timezone.now().date():
            send_message("The borrowings overdue! Fix it!")
        return super().get(request, *args, **kwargs)


class ReturnBorrowingView(generics.UpdateAPIView):
    serializer_class = ReturnBorrowingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(Borrowing, pk=kwargs["pk"])
        if instance.actual_return_date:
            return Response(
                {"error": "The book was already returned before."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        with transaction.atomic():
            instance.actual_return_date = timezone.now().date()
            instance.save()

            book = instance.book
            if book:
                book.inventory += 1
                book.save()

            serializer = self.get_serializer(instance)
            send_message(
                "Successful payment! The book was successfully returned."
            )
            pay_fine(instance)
            return Response(serializer.data)
