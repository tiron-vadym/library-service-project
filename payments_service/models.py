from django.db import models
from django.http import request
from django.urls import reverse

import stripe

from borrowings_service.models import Borrowing


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT"
        FINE = "FINE"

    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    type = models.CharField(
        max_length=10,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT,
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payment"
    )
    session_url = models.URLField(max_length=1000)
    session_id = models.CharField(max_length=55)
    money_to_pay = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.session_url}: {self.status}"
