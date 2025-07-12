from django.urls.conf import path, include

from books_api import views
from books_api.views import ListBookView

urlpatterns = [
    path('books/', ListBookView.as_view(), name='list-books'),
    path('book/', include([
    path('<int:pk>/', views.BookViewSet.as_view(), name='book'),
    ]))
]