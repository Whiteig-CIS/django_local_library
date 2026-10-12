from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [
    path('loanedbooks/', views.LibrarianLoanedBooksView.as_view(), name='books-on-loan'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('study-rooms/', views.StudyRoomListView.as_view(), name='study-rooms'),
    path('study-room/<int:pk>/', views.StudyRoomDetailView.as_view(), name='study-room-detail'),
    path('study-room/create/', views.StudyRoomCreate.as_view(), name='study-room-create'),
    path('study-room/<int:pk>/update/', views.StudyRoomUpdate.as_view(), name='study-room-update'),
    path('study-room/<int:pk>/delete/', views.StudyRoomDelete.as_view(), name='study-room-delete'),
    path('study-room/<int:pk>/reserve/', views.StudyRoomBookingCreate.as_view(), name='study-room-booking-create'),
]

