import stripe
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse


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


def session(price):
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=HttpRequest.build_absolute_uri(reverse("payments-service:success"))
        + f"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=HttpRequest.build_absolute_uri(reverse("payments-service:cancel"))
        + f"?session_id={CHECKOUT_SESSION_ID}",
    )
    return checkout_session


def stripe_helper(borrowing):
    price = calculate_total_amount(borrowing)
    checkout_session = session(price)
    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money_to_pay=price["unit_amount"] / 100,
    )
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

        checkout_session = session(price)
        payment = Payment.objects.create(
            status=Payment.PaymentStatus.PAID,
            type=Payment.PaymentType.FINE,
            borrowing=borrowing,
            session_url=checkout_session.url,
            session_id=checkout_session.id,
            money_to_pay=fine_amount / 100,
        )
        return payment
