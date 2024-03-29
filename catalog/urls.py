from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author-detail'),
]


urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),  # Added for challenge
    # path('myinjuries/', views.InjuriesByUserListView.as_view(), name='my-injuries'),
    path('mybleeds/', views.BleedsByUserListView.as_view(), name='my-bleeds'),
    # path(r'injured/', views.InjuriesAllListView.as_view(), name='all-injuries'),  # Added for challenge
    path(r'bleeds/', views.BleedsAllListView.as_view(), name='all-bleeds'),  # Added for challenge
]


# Add URLConf for librarian to renew a book.
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]


# Add URLConf to create, update, and delete authors
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

# Making my own urls for body injury servey
urlpatterns += [
    path('injury/', views.InjuryListView.as_view(), name='injury'),
]

# Add URLConf to create injurys
urlpatterns += [
    # path('injury/create/', views.create_new_injury, name='injury_create'),
    path('bleed/create/', views.create_new_bleed_ticket, name='bleed_create'),
    # path('injury/<int:pk>', views.InjuryDetailView.as_view(), name='injury-detail'),
    path('bleed/<int:pk>', views.BleedDetailView.as_view(), name='bleedinfo-detail'),
]

# Add URLConf for librarian to renew a book.
urlpatterns += [
    path('injury/renew/', views.create_new_injury, name='create-new-injury'),
]
