from rest_framework import serializers
from books_api.models import Book, Author, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Author

class BookSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Book

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = Book

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        authors_names = [a.get('name') for a in authors]

        existing_authors = Author.objects.filter(name__in=authors_names)

        book = Book.objects.create(**validated_data)
        new_author_names = (
            set(authors_names) - set(existing_authors.values_list('name', flat=True))

        )
        new_authors = [Author(name=name) for name in new_author_names]
        created_authors = Author.objects.bulk_create(new_authors)
        all_authors = list(existing_authors) + list(created_authors)
        book.authors.set(all_authors)

        return book

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Publisher


class PublisherHyperlinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = '__all__'
        model = Publisher

