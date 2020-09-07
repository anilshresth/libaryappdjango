from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# @login_required
def index(request):
    '''view function for the homepage of the site'''
    # generate the count of some main objects
    # for count of the books
    num_books = Book.objects.all().count()
    num_book_instances = BookInstance.objects.all().count()

    # availabel book status
    num_books_availabel = BookInstance.objects.filter(
        status__exact='a').count()
    # all the authors
    num_authors = Author.objects.all().count()

    # Number of visits to the sites as incremented each time the user visits the website
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_book_instances': num_book_instances,
        'num_books_availabel': num_books_availabel,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    # render the template
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    queryset = Book.objects.all()
    paginate_by = 3
    template_name = 'catalog/book_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        # call the base implemenatiton first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # create any data and add it to the context
        context['somedata'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'


class AuthorList(LoginRequiredMixin, generic.ListView):
    model = Author
    login_url = '/accounts/login/'

    # success_url = '/catalog/authors/'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author-detail.html'


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    '''generic class based views listing by the current user'''
    model = BookInstance
    template_name = 'catalog/book_instance_list_borrowed.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(Book, pk)

    # check whether this  is a post request
    if request.method == "POST":
        # create a form instance and populate it with the value from the forms
        form = RenewBookForm()

        # check if the data is valid
        if form.is_valid():
            # process the data in the form.cleaned attribute
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect after succesful submission
            return HttpResponseRedirect('all-borrowed')

    else:
        context = {
            'form': form,
            'book_instance': book_instance,
        }

    return render(request, 'catalog/book_renew_libarian.html', {"form": form})


class AuthorCreate(CreateView):

    model = Author
    fields = '__all__'
    initials = {'date_of_death': '05/01/2018'}


class AuthorUpdate(UpdateView):

    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):

    model = Author
    success_url = reverse_lazy('authors')
