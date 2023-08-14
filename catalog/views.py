from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.views import generic
from catalog.forms import RenewBookForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back'))
    
class LoanedBooksByStaffListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return (BookInstance.objects.filter(status__exact='o').order_by('due_back'))

def catalog(request):
    """View function for home page of site."""
    
    # # # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()
    
    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # # the all() is implied by default, jadi tidak perlu ditulis
    # num_authors = Author.objects.count()
    # genres_name = Genre.objects.all()
    # num_genres = Genre.objects.count()

    # # Session
    # num_visits = request.session.get('num_visit', 0)
    # request.session['num_visit'] = num_visits + 1
    
    # context = {
    #     'num_books': num_books,
    #     'num_instances': num_instances,
    #     'num_instances_available': num_instances_available,
    #     'num_authors': num_authors,
    #     'genres_name': genres_name,
    #     'num_genres': num_genres,
    #     'num_visits': num_visits,
    # }
    
    # Render the HTML template index.html with the data in the context variable

    list_books = get_list_or_404(Book)[-4:]
    list_available_books = get_list_or_404(BookInstance)[-4:]
    list_authors = get_list_or_404(Author)[-4:]
    list_genres = get_list_or_404(Genre)[-4:]

    context = {
        'books': list_books,
        'avail_books': list_available_books,
        'authors': list_authors,
        'genres': list_genres
    }
    
    return render(request, 'catalog/index.html', context=context)

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
    paginate_by = 10

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

@login_required
@permission_required('catalog.cam_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        return render(request, 'catalog/book_renew_librarian.html', context)
    
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

