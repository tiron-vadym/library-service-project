from django.db import models
from django.contrib.auth.models import User

from books_service.models import Book
from customer.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowingb")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowingu")

    def __str__(self):
        return f"Borrowing: {self.book} by User: {self.user}"
