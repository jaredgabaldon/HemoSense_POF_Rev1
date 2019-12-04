from django.shortcuts import render
from django.template import RequestContext
# Create your views here.

from .models import Book, Author, BookInstance, Genre, Injury, Person, Type_Of_Injury, InjuryForm


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_injuries = Injury.objects.all().count()
    num_breaks = Injury.objects.filter(type_of_injury=1).count()
    # Available copies of books
#    num_people_available = BookInstance.objects.filter(status__exact='a').count()
#    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_injuries': num_injuries, 'num_breaks': num_breaks,
                 'num_visits': num_visits},
    )


from django.views import generic

class InjuryListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Injury
    paginate_by = 10

class InjuryDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Injury

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class InjuriesByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = Injury
    template_name = 'catalog/injury_list_by_user.html'

    def get_queryset(self):
        return Injury.objects.filter(person=self.request.user)
    
# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class InjuriesAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Injury
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/injury_list.html'

    def get_queryset(self):
        return Injury.objects.all()


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

# from .forms import RenewBookForm
from catalog.forms import RenewBookForm


    
def create_new_injury(request):
    if request.method == "POST":
        form = InjuryForm(request.POST)
        if form.is_valid():
            injury = form.save(commit=False)
            injury.person = request.user
            injury.save()
            return HttpResponseRedirect(reverse('my-injuries'))
        else:
            variables = RequestContext(request, {'form': form})
            return render(request, 'catalog/injury_form.html', variables)
    else:
        form = InjuryForm(initial={'person': request.user})
    context = {'request': request, 'form': form}
    return render(request, 'catalog/injury_form.html', context)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author, Injury, InjuryForm


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    permission_required = 'catalog.can_mark_returned'

class InjuryCreate(LoginRequiredMixin, CreateView):
    model = Injury
    fields = ['title', 'person', 'summary', 'type_of_injury']
    permission_required = 'catalog.can_mark_returned'

#class InjuryCreate(LoginRequiredMixin):
#    form = InjuryForm(request.POST)
#    if form.is_valid():
#        injury = form.save(commit=False)
#        injury.person = request.user
#        animal.save()

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
