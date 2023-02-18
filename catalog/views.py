from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic import TemplateView
from django.template import loader
# Create your views here.

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5
    

class testView(TemplateView):
    def get(self, request, pk):
        author = Author.objects.get(pk=pk)
        books = Book.objects.filter(author = author).values()
        
        context =  {
            'author': author,
            'books': books
        }
        return render(request, 'catalog/author_detail.html', context= context)
    
class AuthorDetailView(generic.DetailView):
    model = Author
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        self.author = get_object_or_404(Author, pk = self.kwargs['pk'])
        
        context['books'] = Book.objects.filter(author=self.author)
        context['some_data'] = 'this is cool'
        return context
    # def author_detail_view(request, primary_key):
    #     author = get_object_or_404(Author, pk = primary_key)
    #     return render(request, 'catalog/author_detail.html')
    
    
class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    
    context_object_name = 'my_book_list'   # default_name is object_list; your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='War')[:5] # Get 5 books containing the title war
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='Harry')[:5] # Get 5 books containing the title war
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        # try:
        #     book = Book.objects.get(pk=primary_key)
        # except Book.DoesNotExist:
        #     raise Http404('Book does not exist')

        return render(request, 'catalog/book_detail.html', context={'book': book})

    
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    num_genres = Genre.objects.count()
    
    num_books_harry_potter = Book.objects.all().filter(title__contains='Harry Potter').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_harry_potter': num_books_harry_potter,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
