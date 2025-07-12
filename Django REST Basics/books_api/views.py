from django.http.response import JsonResponse
from django.shortcuts import render

from books_api.models import Book
from rest_framework.decorators import api_view


# Create your views here.
# def book(request, pk):
#     book = Book.objects.get(pk=pk)
#     return JsonResponse({
#         "title": book.__dict__.get("title"),
#         "pages": book.__dict__.get("pages"),
#     })

@api_view(['GET'])
def book(request, pk:int):
    book = Book.object.get(pk=pk)