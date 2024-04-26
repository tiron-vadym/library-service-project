from django.urls import path

from borrowings_service.views import (
    BorrowingCreateListView,
    BorrowingDetailView,
    ReturnBorrowingView,
)

app_name = "borrowings_service"

urlpatterns = [
    path("borrowings/", BorrowingCreateListView.as_view(), name="borrowing"),
    path(
        "borrowings/<pk>/",
        BorrowingDetailView.as_view(),
        name="borrowing_detail"
    ),
    path(
        "borrowings/<pk>/return/",
        ReturnBorrowingView.as_view(),
        name="borrowing_return",
    ),
]
