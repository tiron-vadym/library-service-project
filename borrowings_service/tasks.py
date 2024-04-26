from datetime import timezone, timedelta

from celery import shared_task

from borrowings_service.models import Borrowing
from utilities.bot import send_message


@shared_task
def checking_borrowings_overdue() -> None:
    cutoff_date = timezone.now() + timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=cutoff_date, actual_return_date__isnull=True
    )

    if not overdue_borrowings.exists():
        send_message("No borrowings overdue today!")
    for borrowing in overdue_borrowings:
        message_text = (
            f"Overdue Borrowing:\n"
            f"Book Title: {borrowing.book.title}\n"
            f"Borrower: {borrowing.user.username}\n"
            f"Expected Return Date: {borrowing.expected_return_date}\n"
        )
        send_message(message_text)
