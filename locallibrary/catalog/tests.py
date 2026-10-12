from django.test import TestCase
from django.urls import reverse

from .forms import BookForm


class BookStaffCrudTests(TestCase):
    def test_book_form_has_required_fields(self):
        form = BookForm()
        self.assertIn('title', form.fields)
        self.assertIn('author', form.fields)
        self.assertIn('summary', form.fields)
        self.assertIn('isbn', form.fields)

    def test_staff_book_crud_urls_exist(self):
        self.assertEqual(reverse('book-create'), '/catalog/book/create/')
        self.assertEqual(reverse('book-update', args=[1]), '/catalog/book/1/update/')
        self.assertEqual(reverse('book-delete', args=[1]), '/catalog/book/1/delete/')
