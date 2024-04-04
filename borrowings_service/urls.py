from django.urls import path

from borrowings_service.views import (
    BorrowingCreateView,
    BorrowingListView,
    BorrowingDetailView,
    ReturnBorrowingView,
)

app_name = "borrowings_service"

urlpatterns = [
    path("borrowings/", BorrowingCreateView.as_view(), name="borrowing_create"),
    path("borrowings/", BorrowingListView.as_view(), name="borrowing_list"),
    path("borrowings/<pk>/", BorrowingDetailView.as_view(), name="borrowing_detail"),
    path(
        "borrowings/<pk>/return/",
        ReturnBorrowingView.as_view(),
        name="borrowing_return",
    ),
]
