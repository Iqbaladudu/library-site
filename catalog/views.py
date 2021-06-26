from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
# Create your views here.
def index(request):
    """View function for home page of site."""
    
    # # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # the all() is implied by default, jadi tidak perlu ditulis
    num_authors = Author.objects.count()
    genres_name = Genre.objects.all()
    num_genres = Genre.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genres_name': genres_name,
        'num_genres': num_genres,
    }
    
    # Render the HTML template index.html with the data in the context variable
    
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    # this class will get db from models 'Book'
    model = Book
    # your own name for the list as a template variable
    # def get_context_data(self, **kwargs):
    #     # call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # create any data and add it to the context
    #     # context['']
    # context_object_name = 'my_book_list'
    # Get 5 books containing the title war
    def get_queryset(self):
        return Book.objects.all()
    # Specify your own template name/location
    template_name = 'books/book_list.html'
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    def get_queryset(self):
        return Author.objects.all()
    template_name = 'author_list.html'
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author