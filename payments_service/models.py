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

    def pay_fine(self) -> int:
        if self.actual_return_date > self.expected_return_date:
            days_overdue = (
                    self.actual_return_date - self.expected_return_date
            ).days
            fine_amount = int((days_overdue * self.book.daily_fee * 2) * 100)

            price = stripe.Price.create(
                product="prod_Pz5uWC2BXMLDzx",
                unit_amount=fine_amount,
                currency="usd",
            )

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price,
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=request.build_absolute_uri(
                    reverse("payments_service:success")
                )
                + f"?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=request.build_absolute_uri(
                    reverse("payments_service:cancel")
                )
                + f"?session_id={CHECKOUT_SESSION_ID}",
            )
            payment = Payment.objects.create(
                status=Payment.PaymentStatus.PAID,
                type=Payment.PaymentType.FINE,
                borrowing=self,
                session_url=checkout_session.url,
                session_id=checkout_session.id,
                money_to_pay=fine_amount / 100,
            )
            return payment
