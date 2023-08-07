from django import template
from catalog.models import Book, BookInstance, Author, Genre

register = template.Library()

@register.simple_tag()
def get_count(type):
    if type == 'book':
        return Book.objects.all().count()
    elif type == 'book_instance':
        return BookInstance.objects.all().count()
    elif type == 'author':
        return Author.objects.all().count()
    elif type == 'genre':
        return Genre.objects.all().count()