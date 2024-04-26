from rest_framework import serializers

from books_service.serializers import BookSerializer
from borrowings_service.models import Borrowing
from payments_service.serializers import PaymentSerializer


class ExtendedBorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]


class BorrowingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = Borrowing
        fields = [
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment",
        ]


class ReturnBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]
        read_only_fields = [
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]
