from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
import stripe

from borrowings_service.models import Borrowing
from payments_service.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_total_amount(borrowing: Borrowing) -> int:
    using_days = (borrowing.expected_return_date - borrowing.borrow_date).days
    daily_fee_cents = borrowing.book.daily_fee * 100
    looking_price = int(daily_fee_cents) * using_days

    return stripe.Price.create(
        product="prod_Pz5uWC2BXMLDzx",
        unit_amount=looking_price,
        currency="usd",
    )


def session(price, payment):
    request = HttpRequest()
    request.META["SERVER_NAME"] = settings.SERVER_NAME
    request.META["SERVER_PORT"] = settings.SERVER_PORT
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            location=reverse("payments-service:payment-success",
                             kwargs={"pk": payment.id})
        ),
        cancel_url=request.build_absolute_uri(
            location=reverse("payments-service:payment-cancel",
                             kwargs={"pk": payment.id})
        ),
    )
    return checkout_session


def stripe_helper(borrowing):
    price = calculate_total_amount(borrowing)
    payment = Payment.objects.create(
        borrowing=borrowing,
        money_to_pay=price["unit_amount"] / 100,
    )

    checkout_session = session(price, payment)
    payment.session_url = checkout_session.url
    payment.session_id = checkout_session.id
    return payment


def pay_fine(borrowing: Borrowing) -> int:
    if borrowing.actual_return_date > borrowing.expected_return_date:
        days_overdue = (
                borrowing.actual_return_date - borrowing.expected_return_date
        ).days
        fine_amount = int((days_overdue * borrowing.book.daily_fee * 2) * 100)

        price = stripe.Price.create(
            product="prod_Pz5uWC2BXMLDzx",
            unit_amount=fine_amount,
            currency="usd",
        )

        payment = Payment.objects.create(
            status=Payment.PaymentStatus.PAID,
            type=Payment.PaymentType.FINE,
            borrowing=borrowing,
            money_to_pay=fine_amount / 100,
        )
        self = HttpRequest()
        checkout_session = session(self, price, payment)
        payment.session_url = checkout_session.url
        payment.session_id = checkout_session.id
        return payment
