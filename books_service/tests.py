from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from books_service.models import Book


class BookModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@test.com", password="testpass"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="adminpass"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee=1.00,
        )

    def test_str_method(self):
        self.assertEqual(str(self.book), "Test Book by Test Author")

    def test_list_books(self):
        response = self.client.get(reverse("books-service:book-list"))
        self.assertEqual(response.status_code, 200)

    def test_create_book_unauthorized(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.CoverType.SOFT,
            "inventory": 5,
            "daily_fee": 2.00,
        }
        response = self.client.post(reverse("books-service:book-list"), data)
        self.assertEqual(response.status_code, 401)

    def test_create_book_authorized(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "cover": Book.CoverType.SOFT,
            "inventory": 5,
            "daily_fee": 2.00,
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(RefreshToken.for_user(self.admin).access_token)
        )
        response = self.client.post(reverse("books-service:book-list"), data)
        self.assertEqual(response.status_code, 201)

    def test_update_book_unauthorized(self):
        data = {"title": "Updated Book"}
        response = self.client.patch(
            reverse("books-service:book-detail", args=[self.book.id]), data
        )
        self.assertEqual(response.status_code, 401)

    def test_update_book_authorized(self):
        data = {"title": "Updated Book"}
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(RefreshToken.for_user(self.admin).access_token)
        )
        response = self.client.patch(
            reverse("books-service:book-detail", args=[self.book.id]), data
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_book_unauthorized(self):
        response = self.client.delete(
            reverse("books-service:book-detail", args=[self.book.id])
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_book_authorized(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + str(RefreshToken.for_user(self.admin).access_token)
        )
        response = self.client.delete(
            reverse("books-service:book-detail", args=[self.book.id])
        )
        self.assertEqual(response.status_code, 204)
