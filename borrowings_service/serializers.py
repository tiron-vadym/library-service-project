from rest_framework import serializers

from books_service.serializers import BookSerializer
from borrowings_service.models import Borrowing


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
    class Meta:
        model = Borrowing
        fields = [
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
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
