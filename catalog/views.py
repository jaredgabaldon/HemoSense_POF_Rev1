from django.shortcuts import render
from django.template import RequestContext
# Create your views here.

from .models import Book, Author, BookInstance, Genre, Injury, Person, Type_Of_Injury, InjuryForm, BleedInfo, BleedForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

# from .forms import RenewBookForm
from catalog.forms import RenewBookForm


from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib.pagesizes import inch
from reportlab.lib.colors import pink, black, gray, blue, green
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.styles import ParagraphStyle
from pdf_styles import stylesheet


def create_general_info_table():
    table = Table([['title', 'patient', 'ticket_initated_by', 'when_bleed_occured', 'summary', 'bleed_type', 'bleed_location'],
                   ['right arm bleed', 'fake patient', 'fake user', '2019-12-18', 'fake summary', 'spontanous bleed', 'elbow']],
                  colWidths=[1.1 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch])
    table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, gray),
                               ('BOX', (0, 0), (-1, -1), 0.25, black),
                               ('ROWBACKGROUNDS', (0, 0), (-1, 0), [green, gray]),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTSIZE', (1, 0), (-1, -1), 8.5)
                               ]))
    return table
# def create_pdf():
styles = stylesheet()
elements = []
pdf_file_path = 'Macintosh HD/Users/jaredgabaldon/Documents/django_projects/locallibrary/'
pdf_report = SimpleDocTemplate('example report.pdf',
                               pagesize=letter,
                               rightMargin=24,
                               leftMargin=24,
                               topMargin=24,
                               bottomMargin=0.5 * inch)
report_title = Paragraph('hemosense protype pdf', styles['title'])
elements.append(report_title)
data_table = create_general_info_table()
elements.append(data_table)
pdf_report.multiBuild(elements)


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_bleeds = BleedInfo.objects.all().count()
    num_joint_bleeds = BleedInfo.objects.filter(bleed_location=1).count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_bleeds': num_bleeds, 'num_joint_bleeds': num_joint_bleeds,
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

class BleedDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = BleedInfo

class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10

class BleedsListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = BleedInfo
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


class BleedsByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BleedInfo
    template_name = 'catalog/bleedinfo_list_by_user.html'

    def get_queryset(self):
        print(BleedInfo.objects.filter(patient=self.request.user))
        return BleedInfo.objects.filter(patient=self.request.user)


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

@permission_required('catalog.can_mark_returned')
class InjuriesAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Injury
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/injury_list.html'

    def get_queryset(self):
        return Injury.objects.all()




class BleedsAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BleedInfo
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bleedinfo_list.html'

    def get_queryset(self):
        print(BleedInfo.objects.all())
        return BleedInfo.objects.all()


def create_new_injury(request):
    if request.method == "POST":
        form = InjuryForm(request.POST)
        if form.is_valid():
            injury = form.save(commit=False)
            injury.person = request.user
            injury.save()
            return HttpResponseRedirect(reverse('my-bleeds'))
        else:
            variables = RequestContext(request, {'form': form})
            return render(request, 'catalog/bleed_form.html', variables)
    else:
        form = InjuryForm(initial={'person': request.user})
    context = {'request': request, 'form': form}
    return render(request, 'catalog/injury_form.html', context)


def create_new_bleed_ticket(request):
    if request.method == "POST":
        form = BleedForm(request.POST)
        if form.is_valid():
            bleed_info = form.save(commit=False)
            bleed_info.patient = request.user
            bleed_info.save()
            return HttpResponseRedirect(reverse('my-bleeds'))
        else:
            variables = RequestContext(request, {'form': form})
            return render(request, 'catalog/bleed_form.html', variables)
    else:
        form = BleedForm(initial={'person': request.user})
    context = {'request': request, 'form': form}
    return render(request, 'catalog/bleed_form.html', context)

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

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'
