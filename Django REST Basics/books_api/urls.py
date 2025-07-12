from django.urls.conf import path

from books_api import views

urlpatterns = [
    path('book/', views.book, name='book'),
]