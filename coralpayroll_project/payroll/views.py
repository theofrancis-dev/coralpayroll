from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import datetime

from .models import Business
from .models import Address, Person, Employment
from .models import Earnings

from .forms import AddressForm, PersonForm
from .forms import BusinessUpdateForm, BusinessCreateForm
from .forms import EarningsForm




#======================== BUSINESS SECTION =========================================
class BusinessListView(LoginRequiredMixin, ListView):
    model = Business
    template_name = 'business_list.html'  # Ensure you have a template named business_list.html
    context_object_name = 'businesses'
    paginate_by = 10  # Number of businesses per page

    def get_queryset(self):
        # Retrieve all businesses and order them by entity_name
        return Business.objects.all().order_by('entity_name')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the selected business_id from the session
        business_id = self.request.session.get('selected_business_id')
        if business_id:
            # Retrieve the business instance or return None if not found
            context['selected_business'] = get_object_or_404(Business, pk=business_id)
        else:
            context['selected_business'] = None
        return context
    
@login_required
def business_detail(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    
    # Save the business ID in the session
    request.session['selected_business_id'] = business_id

    context = {
        'business': business,
        'staff': Person.objects.filter(business=business),
    }
    return render(request, 'business_detail.html', context)

@login_required
def business_update(request, pk):
    business = get_object_or_404(Business, pk=pk)
    if request.method == 'POST':
        form = BusinessUpdateForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business-detail', pk=pk)  # Redirect to the business detail view after updating
    else:
        form = BusinessUpdateForm(instance=business)
    return render(request, 'business_update.html', {'form': form, 'business': business})

@login_required
def create_business(request):
    if request.method == 'POST':
        form = BusinessCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business-list')  # Redirect to the business list view after creating a new business
    else:
        form = BusinessCreateForm()
    return render(request, 'create_business.html', {'form': form})

#===================== CLIENT SECTION ==================================================
@login_required
def create_client(request):
    PersonFormSet = inlineformset_factory(Address, Person, form=PersonForm, extra=1, can_delete=False)
    
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        formset = PersonFormSet(request.POST)
        
        if address_form.is_valid() and formset.is_valid():
            address = address_form.save()
            persons = formset.save(commit=False)
            for person in persons:
                person.address = address
                person.save()
            return redirect('list-clients')  # Adjust this to your desired redirect target
    else:
        address_form = AddressForm()
        formset = PersonFormSet()

    return render(request, 'create_client.html', {'address_form': address_form, 'formset': formset})

@login_required
def list_clients(request):
    business_id = request.session.get('selected_business_id')
    business = get_object_or_404(Business, pk=business_id) if business_id else None
    

    clients_list = Person.objects.all().order_by('first_name')  # Order by first name
    paginator = Paginator(clients_list, 10)  # Show 10 clients per page

    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)

    context = {
        'clients': clients,
        'business': business,
    }
    return render(request, 'list_clients.html', context)

# client(Person) detailed view
@login_required
def client_detail(request, pk):
    client = get_object_or_404(Person, pk=pk)
    return render(request, 'client_detail.html', {'client': client})

#client update and delete views
# Update view
@login_required
def update_client(request, pk):
    client = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client-detail', pk=client.pk)
    else:
        form = PersonForm(instance=client)
    return render(request, 'update_client.html', {'form': form})

# Delete view
@login_required
def delete_client(request, pk):
    client = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('list-clients')
    return render(request, 'delete_client.html', {'client': client})


#=========================   STAFF SECTION ================================================
#staff list view
@login_required
def list_staff(request, business_id):
    # get current business
    # business_id = request.session.get('selected_business_id')
    # business = get_object_or_404(Business, pk=business_id) if business_id else None
    # Filter by the many-to-many relationship
    staff = Person.objects.filter(businesses__id=business_id)  

    context = {
        'staff': staff,       
        'business_id': business_id,
    }
    return render(request, 'list_staff.html', context)

@login_required
def add_staff(request, person_id):
    business_id = request.session.get('selected_business_id')
    business = get_object_or_404(Business, pk=business_id)
    client = get_object_or_404(Person, pk=person_id)
    
    # Add the client to the business (create the relationship)
    Employment.objects.create(person=client, business=business)
    
    return redirect('list_staff', business_id=business.id)

@login_required
def remove_staff(request, business_id, person_id):
    # Remove the person from the business
    employment = get_object_or_404(Employment, business_id=business_id, person_id=person_id)
    employment.delete()  # This will remove the relationship but keep the person and business records

    return redirect('list_staff', business_id=business_id)

@login_required
def add_earnings(request, business_id, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        form = EarningsForm(request.POST)
        if form.is_valid():
            earnings = form.save(commit=False)
            earnings.business_id = business_id
            earnings.person_id = person_id
            earnings.save()
            return redirect('list_staff', business_id=business_id)
    else:
        form = EarningsForm(initial={'employee_name': f'{person.first_name} {person.last_name}'})
    
    context = {
        'form': form,
        'person': person,
    }
    return render(request, 'add_earnings.html', context)


# views.py

from django.core.paginator import Paginator
from datetime import datetime

# views.py

@login_required
def view_earnings(request, business_id, person_id):
    person = get_object_or_404(Person, pk=person_id)
    current_year = datetime.now().year
    year = request.GET.get('year', current_year)
    earnings = Earnings.objects.filter(business_id=business_id, person_id=person_id, date__year=year).order_by('-date')

    paginator = Paginator(earnings, 10)  # Show 10 earnings per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Create a range of years from 2020 to 2050
    year_range = range(2020, 2051)

    context = {
        'person': person,
        'earnings': earnings,
        'page_obj': page_obj,
        'business_id': business_id,
        'year': int(year),
        'current_year': current_year,
        'year_range': year_range,
    }
    return render(request, 'view_earnings.html', context)


@login_required
def delete_earning(request, business_id, earning_id):
    earning = get_object_or_404(Earnings, pk=earning_id)
    person_id = earning.person_id
    earning.delete()
    return HttpResponseRedirect(reverse('view_earnings', args=[business_id, person_id]))

@login_required
def update_earning(request, business_id, earning_id):
    earning = get_object_or_404(Earnings, pk=earning_id)
    person = earning.person
    if request.method == 'POST':
        form = EarningsForm(request.POST, instance=earning)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_earnings', args=[business_id, person.id]))
    else:
        form = EarningsForm(instance=earning)
    
    context = {
        'form': form,
        'person': person,
        'business_id': business_id,
    }
    return render(request, 'update_earning.html', context)

