from django.urls.conf import path, include

from books_api import views

urlpatterns = [

    path('book/', include([
    path('<int:pk>/', views.BookViewSet.as_view(), name='book'),
    ]))
]