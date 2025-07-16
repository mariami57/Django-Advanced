from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from books_api.models import Book, Publisher
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, views, generics, viewsets
from books_api.serializers import BookSerializer, BookSimpleSerializer, PublisherSerializer, \
    PublisherHyperlinkSerializer


# Create your views here.
# def book(request, pk):
#     book = Book.objects.get(pk=pk)
#     return JsonResponse({
#         "title": book.__dict__.get("title"),
#         "pages": book.__dict__.get("pages"),
#     })

# @api_view(['GET'])
# def get_book(request, pk:int):
#     book = Book.objects.get(pk=pk)
#     serializer = BookSerializer(book)
#     return Response(serializer.data, status=status.HTTP_200_OK)

class ListBookView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.prefetch_related('authors')

class BookViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSimpleSerializer
    queryset = Book.objects.all()


    # def get_object(self, pk):
    #     return get_object_or_404(Book, pk=pk)

    # def get(self,request, pk):
    #     book = self.get_object(pk)
    #     serializer = self.serializer(book)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def put(self,request, pk):
    #     book = self.get_object(pk)
    #     serializer = self.serializer(instance=book, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def patch(self,request,pk):
    #     book = self.get_object(pk)
    #     serializer = self.serializer(instance=book, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def delete(self,request,pk):
    #     book = self.get_object(pk)
    #     book.delete()
    #     return Response(status=status.HTTP_200_OK)



@api_view(['POST'])
def create_book(request):
    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class PublisherHyperLinkView(generics.ListAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherHyperlinkSerializer